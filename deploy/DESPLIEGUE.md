# Despliegue de Burke Export en el servidor

Guía para actualizar producción sin afectar otros servicios del servidor (por ejemplo, OrderClic).

## Reglas de convivencia

- Trabaja **solo** dentro de la carpeta de este proyecto y con su proyecto de Docker Compose.
- No uses `docker system prune`, `docker volume prune`, `docker compose down -v` ni borres volúmenes, imágenes o redes de otros proyectos.
- No cambies el nombre de la carpeta, el nombre del servicio `db` ni el volumen `db_data`, y no pases `-p`: Compose crearía una base de datos **vacía** con otro nombre.
- La app solo escucha en `127.0.0.1:${WEB_PORT}` (8001 por defecto). Si ese puerto lo usa otro servicio, cambia `WEB_PORT` en `.env` y el `proxy_pass` de nginx.
- En nginx, edita **solo** el bloque de `burkeexport.com`. Ejecuta `nginx -t` antes de recargar.

## Qué cambia en esta versión

- MariaDB pasa de 10.9 a 11.4 LTS. La actualización del volumen es automática (`MARIADB_AUTO_UPGRADE`), pero **hay que respaldar antes**.
- El `.env` deja de estar en git: **`git pull` lo borra**. Hay que respaldarlo antes.
- Variables nuevas en `.env`: `FORCE_HTTPS`, `ADMIN_URL`, `SERVE_MEDIA`, `DB_ROOT_PASSWORD` y `WEB_PORT` (ver `.env.example`). La `SECRET_KEY` debe ser nueva y tener al menos 50 caracteres.
- `./staticfiles` ya no se monta: los estáticos van dentro de la imagen y los sirve WhiteNoise. Si nginx tiene un `location /static/` apuntando a esa carpeta, quítalo.
- El admin se mueve a `/${ADMIN_URL}`. `/admin/` devuelve 404.
- Las URLs en inglés pasan a `/en/...`. Las de español no cambian.

## Pasos

1. Haz un inventario de lo que corre (`docker ps`, `docker compose ls`, `ss -ltnp`) para poder comparar al final.
2. Respalda el `.env`, un dump de la BD y una copia del volumen.
3. Ejecuta `git pull`, restaura el `.env` y complétalo.
4. Ejecuta `docker compose build --pull`, ajusta los permisos de `media/` y luego `docker compose up -d --wait`, `migrate` y `check --deploy`.
5. Ajusta nginx si hace falta.
6. Verifica el sitio, el admin y que los demás servicios siguen igual.
7. Crea el usuario del cliente con `python manage.py crear_editor <usuario>`.

## Volver atrás

1. `docker compose down` (sin `-v`).
2. `git checkout 53f2cb7`.
3. Restaura el `.env` respaldado.
4. Restaura la copia del volumen: la versión anterior usa MariaDB 10.9, que no abre datos ya actualizados a 11.4.
5. `docker compose up -d --build`.
