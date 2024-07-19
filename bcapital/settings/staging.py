import sys

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
        'NAME': os.environ.get('DB_NAME_STAGING'),
        'USER': os.environ.get('DB_USER_STAGING'),
        'PASSWORD': os.environ.get('DB_PASSWORD_STAGING'),
        'HOST': os.environ.get('DB_HOST_STAGING'),
        'PORT': os.environ.get('DB_PORT')
    },
}
#DATABASECONECCTION
DB_NAME_DEV = os.environ.get('DB_NAME_STAGING')
DB_USER_DEV = os.environ.get('DB_USER_STAGING')
DB_PASSWORD_DEV = os.environ.get('DB_PASSWORD_STAGING')
DB_HOST_DEV = os.environ.get('DB_HOST_STAGING')
DB_PORT = os.environ.get('DB_PORT')

# Configuration for local test on Databse SQLite 3
if "test" in sys.argv or "test_coverage" in sys.argv:
    DATABASES["default"]["ENGINE"] = "django.db.backends.sqlite3"

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = "/static/"

STATICFILES_STORAGE = "bcapital.storage.StaticStorage"
DEFAULT_FILE_STORAGE = "bcapital.storage.MediaStorage"
AWS_STORAGE_BUCKET_NAME = 'dashboard-backend-api'