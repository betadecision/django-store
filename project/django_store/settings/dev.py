"""
Local development settings.
"""

import os

from .base import BASE_DIR
from .base import *  # noqa: F403


SECRET_KEY = os.getenv(
    "DJANGO_SECRET_KEY",
    "django-insecure-2uhwlvkhfx97+c=p86g2-5cdpgenqv(8$%wgl(9va2ujue=(&9",
)

DEBUG = True

ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

