"""
Test settings.
"""

from .base import BASE_DIR
from .base import *  # noqa: F403


SECRET_KEY = "django-test-secret-key"

DEBUG = False

ALLOWED_HOSTS = ["testserver"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "test.sqlite3",
    }
}

