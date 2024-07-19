#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import pycron
from pathlib import Path
from environ import environ
from barter_backend.services.cronjobs.CronSchedules import *
from barter_backend.core.CreateSchema import *

BASE_DIR = Path(__file__).resolve().parent.parent
env = environ.Env()
environ.Env.read_env()

#root = environ.Path(start=__file__)
#env = environ.Env()
#env.read_env(".env")



def main():    
    """Run administrative tasks."""
    if sys.argv[1] == "test":
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bcapital.settings.test")
    else:
        if env.bool("APP_DEBUG"):
            os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bcapital.settings.dev")
        else:
            os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bcapital.settings.prod")
    #os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bcapital.settings.dev_new")
    
    try:
        from django.core.management import execute_from_command_line        
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    #do()    
    execute_from_command_line(sys.argv)
    


if __name__ == "__main__":
    main()    
