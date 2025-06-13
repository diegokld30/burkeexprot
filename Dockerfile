# Usa Python 3.13 slim
FROM python:3.13-slim

# Desactiva buffering y apunta al settings de producción
ENV PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=burkeExport.settings

WORKDIR /app

# Instala dependencias para compilar mysqlclient
RUN apt-get update \
 && apt-get install -y \
      build-essential \
      default-libmysqlclient-dev \
      pkg-config \
      python3-dev \
    --no-install-recommends \
 && rm -rf /var/lib/apt/lists/*

# Copia e instala tus dependencias Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt \
 && pip install --no-cache-dir mysqlclient

# Copia el resto del código
COPY . .

# Genera los archivos estáticos
RUN python manage.py collectstatic --noinput

EXPOSE 8000

# Arranca Gunicorn apuntando al WSGI de tu proyecto
CMD ["gunicorn", "burkeExport.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]
