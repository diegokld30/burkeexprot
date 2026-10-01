#!/bin/bash
set -euo pipefail

ENVIRONMENT=${1:-}

if [ -z "$ENVIRONMENT" ]; then
  echo "❌ Debes especificar el entorno: dev o prod"
  exit 1
fi

if [ ! -f .env ]; then
  echo "❌ Falta el archivo .env (copia .env.example y complétalo)"
  exit 1
fi

# Docker Compose v2 ("docker compose") o v1 ("docker-compose")
if docker compose version &> /dev/null; then DC="docker compose"; else DC="docker-compose"; fi

if [ "$ENVIRONMENT" = "dev" ]; then
  FILE=docker-compose.dev.yml
  echo "🚧 Levantando entorno de DESARROLLO..."
  $DC -f $FILE up -d --build --wait

  echo "🛠️ Aplicando migraciones..."
  $DC -f $FILE exec web python manage.py migrate

  echo "📂 Para crear un superusuario:"
  echo "$DC -f $FILE exec web python manage.py createsuperuser"
  echo "🎨 CSS: ejecuta 'npm run watch:css' en otra terminal"

  echo "🌐 http://127.0.0.1:8000"
  echo "📜 Logs en tiempo real (Ctrl+C para salir)"
  $DC -f $FILE logs -f web

elif [ "$ENVIRONMENT" = "prod" ]; then
  FILE=docker-compose.yml
  WEB_PORT=$(grep -E "^WEB_PORT=" .env | cut -d= -f2 || true)
  echo "🚀 Construyendo imagen de PRODUCCIÓN (con parches de seguridad al día)..."
  $DC -f $FILE build --pull

  echo "🔐 Ajustando permisos de media/ para el usuario sin privilegios..."
  mkdir -p media
  $DC -f $FILE run --rm --no-deps --user root --entrypoint chown web -R 10001:10001 /app/media

  echo "⏳ Levantando servicios..."
  $DC -f $FILE up -d --wait

  echo "🛠️ Aplicando migraciones..."
  $DC -f $FILE exec web python manage.py migrate --noinput

  echo "🔎 Verificación de seguridad de Django..."
  $DC -f $FILE exec web python manage.py check --deploy

  echo "🌐 Producción disponible en http://127.0.0.1:${WEB_PORT:-8001} (detrás de nginx)"
  echo "📜 Logs en tiempo real (Ctrl+C para salir)"
  $DC -f $FILE logs -f web

else
  echo "❌ Entorno no reconocido. Usa 'dev' o 'prod'"
  exit 1
fi
