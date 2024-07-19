from django.core.management import BaseCommand
from django.db import transaction


class Command(BaseCommand):
    help = 'Actualizar el plan de ganancias de los usuarios'

    @transaction.atomic()
    def handle(self, *args, **options):
        try:
            print('Iniciando actualización de plan de trading de los usuarios')



        except Exception as e:
            print(e)
            raise e
