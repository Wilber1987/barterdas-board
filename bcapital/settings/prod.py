"""Module providing access to argv array"""
import os
from .base import *

ALLOWED_HOSTS = ["*"]  # TODO: NO PERMITIR APARTE DEL DOMINIO DE FRONTEND

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('DB_NAME_PROD'),
        'USER': os.environ.get('DB_USER_PROD'),
        'PASSWORD': os.environ.get('DB_PASSWORD_PROD'),
        'HOST': os.environ.get('DB_HOST_PROD'),
        'PORT': os.environ.get('DB_PORT')
    },
}
#DATABASECONECCTION
DB_NAME_DEV = os.environ.get('DB_NAME_PROD')
DB_USER_DEV = os.environ.get('DB_USER_PROD')
DB_PASSWORD_DEV = os.environ.get('DB_PASSWORD_PROD')
DB_HOST_DEV = os.environ.get('DB_HOST_PROD')
DB_PORT = os.environ.get('DB_PORT')

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = "/static/"

STATICFILES_STORAGE = "bcapital.storage.StaticStorageProd"
DEFAULT_FILE_STORAGE = "bcapital.storage.MediaStorageProd"
AWS_STORAGE_BUCKET_NAME = 'dashboard-backend-api-prod'
