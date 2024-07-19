"""Module providing access to argv array"""
import sys
import os
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()

from .base import *



DEBUG = True

ALLOWED_HOSTS = []

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(Path(__file__).resolve().parent.parent.parent, "db.sqlite3"),
    }
}

# Configuration for local test on Databse SQLite 3
if "test" in sys.argv or "test_coverage" in sys.argv:
    DATABASES["default"]["ENGINE"] = "django.db.backends.sqlite3"

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = "/static/"

# USE TO DISABLE FILE PROCESSING WHEN ON TEST MODE
TESTING_MODE = True
