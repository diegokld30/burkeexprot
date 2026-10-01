# syntax=docker/dockerfile:1

# ─── 1. CSS: compila Tailwind con las clases usadas en las plantillas ───
FROM node:24-slim AS css
WORKDIR /src
COPY package.json package-lock.json ./
RUN npm ci --no-audit --no-fund
COPY assets assets
COPY templates templates
COPY core/static/js core/static/js
RUN npm run build:css

# ─── 2. Dependencias Python (con compiladores, no llegan a la imagen final) ───
FROM python:3.13-slim AS builder
RUN apt-get update \
 && apt-get install -y --no-install-recommends build-essential default-libmysqlclient-dev pkg-config \
 && rm -rf /var/lib/apt/lists/*
RUN python -m venv /opt/venv
ENV PATH=/opt/venv/bin:$PATH
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
 && pip install --no-cache-dir -r requirements.txt

# ─── 3. Imagen final: mínima y sin root ───
FROM python:3.13-slim
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH=/opt/venv/bin:$PATH \
    DJANGO_SETTINGS_MODULE=burkeExport.settings

RUN apt-get update \
 && apt-get upgrade -y \
 && apt-get install -y --no-install-recommends libmariadb3 gettext \
 && rm -rf /var/lib/apt/lists/* \
 && useradd --system --uid 10001 --no-create-home --shell /usr/sbin/nologin app

WORKDIR /app
COPY --from=builder /opt/venv /opt/venv
COPY . .
COPY --from=css /src/core/static/css/tailwind.css core/static/css/tailwind.css

# Compila traducciones y estáticos (clave temporal solo para el build)
RUN export SECRET_KEY="build-only-$(python -c 'import secrets;print(secrets.token_hex(32))')" \
 && python manage.py compilemessages \
 && python manage.py collectstatic --noinput \
 && apt-get purge -y gettext && apt-get autoremove -y \
 && mkdir -p /app/media && chown -R app:app /app/media

USER app
EXPOSE 8000
CMD ["gunicorn", "burkeExport.wsgi:application", \
     "--bind", "0.0.0.0:8000", "--workers", "3", "--timeout", "30", \
     "--max-requests", "1000", "--max-requests-jitter", "100", \
     "--access-logfile", "-", "--error-logfile", "-"]
