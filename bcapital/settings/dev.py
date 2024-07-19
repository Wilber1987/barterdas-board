"""Module providing access to argv array"""
import sys
import os
from .base import *


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    "*",
]

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('DB_NAME_DEV'),
        'USER': os.environ.get('DB_USER_DEV'),
        'PASSWORD': os.environ.get('DB_PASSWORD_DEV'),
        'HOST': os.environ.get('DB_HOST_DEV'),
        'PORT': os.environ.get('DB_PORT')
    },
}

#DATABASECONECCTION
DB_NAME_DEV = os.environ.get('DB_NAME_DEV')
DB_USER_DEV = os.environ.get('DB_USER_DEV')
DB_PASSWORD_DEV = os.environ.get('DB_PASSWORD_DEV')
DB_HOST_DEV = os.environ.get('DB_HOST_DEV')
DB_PORT = os.environ.get('DB_PORT')

DB_PASSWORD_DEV = "Desarrollo2024%"
DB_NAME_DEV = "postgres"
DB_HOST_DEV = "bartercbd2024.postgres.database.azure.com"
DB_USER_DEV = "barterc"
DB_PORT = 5432


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': DB_NAME_DEV,
        'USER': DB_USER_DEV,
        'PASSWORD': DB_PASSWORD_DEV,
        'HOST': DB_HOST_DEV,
        'PORT': DB_PORT,
    },
}

# Configuration for local test on Databse SQLite 3
if "test" in sys.argv or "test_coverage" in sys.argv:
    DATABASES["default"]["ENGINE"] = "django.db.backends.sqlite3"

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = "/static/"

STATICFILES_STORAGE = "bcapital.storage.StaticStorage"
DEFAULT_FILE_STORAGE = "bcapital.storage.MediaStorage"
AWS_STORAGE_BUCKET_NAME = 'dashboard-backend-api'