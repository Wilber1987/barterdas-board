from django.core.management import BaseCommand
from django.db import transaction

from barter_auth.models import BarterUser
from global_settings.models import RootBarterUser


class Command(BaseCommand):
    help = 'Actualizar la red de usuarios, si no tiene patrocinador se le asigna el usuario admin'

    @transaction.atomic()
    def handle(self, *args, **options):
        try:
            users = BarterUser.objects.filter(unilevel_network_in__isnull=True)
            user_root = RootBarterUser.objects.filter(enabled=True).first()
            print('Cantidad de usuarios sin red: ', users.count())
            for user in users:
                # TODO: crear lógica para asignar el usuario root como patrocinador
                pass

        except Exception as e:
            print(e)
            raise e
