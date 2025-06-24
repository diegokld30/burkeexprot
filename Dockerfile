# syntax=docker/dockerfile:1

# ─── 1. Imagen base ─────────────────────────────────────────────
FROM python:3.13-slim

# ─── 2. Variables de entorno ────────────────────────────────────
ENV PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=burkeExport.settings

WORKDIR /app

# ─── 3. Dependencias de sistema ─────────────────────────────────
#    * gettext ➜ aporta `msgfmt` para compilemessages
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        default-libmysqlclient-dev \
        pkg-config \
        python3-dev \
        gettext \
    && rm -rf /var/lib/apt/lists/*

# ─── 4. Dependencias Python ─────────────────────────────────────
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt \
 && pip install --no-cache-dir mysqlclient

# ─── 5. Copia del proyecto ──────────────────────────────────────
COPY . .

# ─── 6. Compila catálogos + genera staticfiles ──────────────────
RUN python manage.py compilemessages \
 && python manage.py collectstatic --noinput

# ─── 7. Exposición y arranque ───────────────────────────────────
EXPOSE 8000
CMD ["gunicorn", "burkeExport.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]
