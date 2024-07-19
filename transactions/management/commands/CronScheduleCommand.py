from django.core.management.base import BaseCommand
from barter_backend.services.cronjobs.CronSchedules import main
import threading
class Command(BaseCommand):
    help = 'Run pycron for scheduled tasks'

    def handle(self, *args, **options):
        cron_thread = threading.Thread(target=main)
        # Inicia el hilo
        cron_thread.start()
        # Espera a que el hilo termine (si es necesario)
        cron_thread.join()