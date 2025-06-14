#!/bin/bash

ENVIRONMENT=$1

if [ -z "$ENVIRONMENT" ]; then
  echo "❌ Debes especificar el entorno: dev o prod"
  exit 1
fi

function wait_for_db() {
  echo "⏳ Esperando a que la base de datos esté disponible..."
  until docker exec "$1" mariadb -u root -p"rootpassword" -e "SELECT 1" &> /dev/null; do
    sleep 2
  done
  echo "✅ Base de datos lista."
}

function get_container() {
  docker-compose -f "$1" ps -q "$2"
}

if [ "$ENVIRONMENT" = "dev" ]; then
  echo "🚧 Levantando entorno de DESARROLLO..."
  docker-compose -f docker-compose.dev.yml up -d --build

  sleep 3
  DB_CONTAINER=$(get_container docker-compose.dev.yml db)
  WEB_CONTAINER=$(get_container docker-compose.dev.yml web)

  if [ -z "$DB_CONTAINER" ] || [ -z "$WEB_CONTAINER" ]; then
    echo "❌ No se encontraron los contenedores."
    docker ps -a
    exit 1
  fi

  wait_for_db "$DB_CONTAINER"

  echo "🛠️ Aplicando migraciones..."
  docker exec "$WEB_CONTAINER" python manage.py migrate

  echo "📂 Verifica si necesitas crear un superusuario:"
  echo "docker exec $WEB_CONTAINER python manage.py createsuperuser"

  echo "🌐 Abriendo navegador en http://127.0.0.1:8000"
  if command -v xdg-open &> /dev/null; then
    xdg-open http://127.0.0.1:8000
  elif command -v open &> /dev/null; then
    open http://127.0.0.1:8000
  fi

  echo "📜 Logs en tiempo real (Ctrl+C para salir)"
  docker-compose -f docker-compose.dev.yml logs -f web

elif [ "$ENVIRONMENT" = "prod" ]; then
  echo "🚀 Levantando entorno de PRODUCCIÓN..."
  docker-compose -f docker-compose.yml up -d --build

  sleep 3
  DB_CONTAINER=$(get_container docker-compose.yml db)
  WEB_CONTAINER=$(get_container docker-compose.yml web)

  if [ -z "$DB_CONTAINER" ] || [ -z "$WEB_CONTAINER" ]; then
    echo "❌ No se encontraron los contenedores."
    docker ps -a
    exit 1
  fi

  wait_for_db "$DB_CONTAINER"

  echo "🛠️ Aplicando migraciones..."
  docker exec "$WEB_CONTAINER" python manage.py migrate

  echo "📦 Recolectando archivos estáticos..."
  docker exec "$WEB_CONTAINER" python manage.py collectstatic --noinput

  echo "🌐 Producción disponible en http://127.0.0.1:8001"
  echo "📜 Logs en tiempo real (Ctrl+C para salir)"
  docker-compose -f docker-compose.yml logs -f web

else
  echo "❌ Entorno no reconocido. Usa 'dev' o 'prod'"
  exit 1
fi
