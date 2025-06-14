from .settings import *

DEBUG = True
ALLOWED_HOSTS = ["*"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "burkeexport",
        "USER": "burkeuser",
        "PASSWORD": "burkeexport123",
        "HOST": "127.0.0.1",
        "PORT": "3306",
        "OPTIONS": {
            "init_command": "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}
