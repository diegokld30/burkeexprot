import os
from datetime import timedelta
from pathlib import Path

from django.core.exceptions import ImproperlyConfigured


def env_bool(name, default=False):
    return os.environ.get(name, str(default)).strip().lower() in ("true", "1", "yes")


def env_list(name, default=""):
    return [v.strip() for v in os.environ.get(name, default).split(",") if v.strip()]


# ───────── Base ─────────
BASE_DIR = Path(__file__).resolve().parent.parent

# ───────── Entorno ─────────
# Seguro por defecto: si falta el .env la app NO arranca en modo debug.
DEBUG = env_bool("DEBUG", False)

SECRET_KEY = os.environ.get("SECRET_KEY", "")
if not SECRET_KEY:
    if not DEBUG:
        raise ImproperlyConfigured("Falta SECRET_KEY en el entorno (.env).")
    SECRET_KEY = "dev-only-insecure-key"
elif not DEBUG and (SECRET_KEY.startswith("django-insecure") or len(SECRET_KEY) < 50):
    raise ImproperlyConfigured("SECRET_KEY insegura: genera una nueva (ver .env.example).")

# ALLOWED_HOSTS desde .env, p. ej. "burkeexport.com,www.burkeexport.com"
ALLOWED_HOSTS = env_list("ALLOWED_HOSTS")

# Ruta del panel de administración (cámbiala en .env para esconderla de bots)
ADMIN_URL = os.environ.get("ADMIN_URL", "admin/").strip("/") + "/"

# ───────── Aplicaciones y Middleware ─────────
INSTALLED_APPS = [
    'modeltranslation',  # debe ir antes de tu app
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',
    'axes',  # bloqueo de ataques de fuerza bruta al login
    'core',  # tu app principal
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",
    'core.middleware.SecurityHeadersMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'axes.middleware.AxesMiddleware',  # debe ir al final
]

AUTHENTICATION_BACKENDS = [
    'axes.backends.AxesStandaloneBackend',  # debe ir primero
    'django.contrib.auth.backends.ModelBackend',
]

ROOT_URLCONF = 'burkeExport.urls'
WSGI_APPLICATION = 'burkeExport.wsgi.application'

# ───────── Templates ─────────
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.i18n',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'core.context_processors.seo',
            ],
        },
    },
]

# ───────── Base de datos MySQL/MariaDB ─────────
DATABASES = {
    "default": {
        "ENGINE": os.getenv("DATABASE_ENGINE", "django.db.backends.sqlite3"),
        "NAME":   os.getenv("DATABASE_NAME", BASE_DIR / "db.sqlite3"),
        "USER":   os.getenv("DATABASE_USER", ""),
        "PASSWORD": os.getenv("DATABASE_PASSWORD", ""),
        "HOST":   os.getenv("DATABASE_HOST", ""),   # ← ¡no hard-codear 127.0.0.1!
        "PORT":   os.getenv("DATABASE_PORT", ""),
        "CONN_MAX_AGE": 60,
    }
}
if "mysql" in DATABASES["default"]["ENGINE"]:
    DATABASES["default"]["OPTIONS"] = {
        "init_command": "SET sql_mode='STRICT_TRANS_TABLES'",
        "charset": "utf8mb4",
    }

# ───────── Validación de contraseñas ─────────
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
     'OPTIONS': {'min_length': 12}},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ───────── Internacionalización ─────────
LANGUAGE_CODE = 'es'
LANGUAGES = [
    ('es', 'Español'),
    ('en', 'English'),
]
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True
LOCALE_PATHS = [BASE_DIR / 'locale']

# ───────── Archivos estáticos y media ─────────
# core/static lo encuentra AppDirectoriesFinder (core es una app instalada).
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
# Sirve /media/ desde Django si nginx no lo hace (ver deploy/nginx-burkeexport.conf)
SERVE_MEDIA = env_bool("SERVE_MEDIA", True)

STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {
        "BACKEND": (
            "django.contrib.staticfiles.storage.StaticFilesStorage" if DEBUG
            else "whitenoise.storage.CompressedManifestStaticFilesStorage"
        ),
    },
}

# Límite de subida (imágenes del admin)
DATA_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024
FILE_UPLOAD_MAX_MEMORY_SIZE = 5 * 1024 * 1024

# ───────── Seguridad HTTPS, cookies y cabeceras ─────────
# FORCE_HTTPS=False solo para probar en local sin certificado. En producción: True.
FORCE_HTTPS = env_bool("FORCE_HTTPS", True) and not DEBUG

SECURE_SSL_REDIRECT = FORCE_HTTPS
SESSION_COOKIE_SECURE = FORCE_HTTPS
CSRF_COOKIE_SECURE = FORCE_HTTPS
LANGUAGE_COOKIE_SECURE = FORCE_HTTPS
SECURE_HSTS_SECONDS = 31536000 if FORCE_HTTPS else 0
SECURE_HSTS_INCLUDE_SUBDOMAINS = FORCE_HTTPS
SECURE_HSTS_PRELOAD = FORCE_HTTPS

SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_REFERRER_POLICY = "strict-origin-when-cross-origin"
X_FRAME_OPTIONS = "DENY"
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_AGE = 60 * 60 * 8  # sesiones del admin: 8 horas
LANGUAGE_COOKIE_SAMESITE = "Lax"

# Confía en estos orígenes para CSRF
CSRF_TRUSTED_ORIGINS = [f"https://{h}" for h in ALLOWED_HOSTS]

# Avisa a Django que confíe en la cabecera X-Forwarded-Proto (la pone nginx)
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Content-Security-Policy (aplicada en core.middleware.SecurityHeadersMiddleware)
CONTENT_SECURITY_POLICY = "; ".join([
    "default-src 'self'",
    "script-src 'self'",
    "style-src 'self' 'unsafe-inline'",
    "img-src 'self' data:",
    "font-src 'self' data:",
    "connect-src 'self'",
    "object-src 'none'",
    "base-uri 'self'",
    "form-action 'self'",
    "frame-ancestors 'none'",
])

# ───────── Protección contra fuerza bruta (django-axes) ─────────
AXES_FAILURE_LIMIT = 5                    # intentos fallidos permitidos
AXES_COOLOFF_TIME = timedelta(hours=1)    # tiempo de bloqueo
AXES_LOCKOUT_PARAMETERS = ["ip_address"]
AXES_RESET_ON_SUCCESS = True
# Detrás de nginx: la IP real es la última añadida a X-Forwarded-For
AXES_IPWARE_PROXY_COUNT = 1
AXES_IPWARE_META_PRECEDENCE_ORDER = ["HTTP_X_FORWARDED_FOR", "REMOTE_ADDR"]

# ───────── Logs a la consola (docker logs) ─────────
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {"console": {"class": "logging.StreamHandler"}},
    "root": {"handlers": ["console"], "level": "WARNING"},
    "loggers": {
        "django": {"handlers": ["console"], "level": "WARNING", "propagate": False},
        "axes": {"handlers": ["console"], "level": "WARNING", "propagate": False},
    },
}

# ───────── Default primary key ─────────
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
