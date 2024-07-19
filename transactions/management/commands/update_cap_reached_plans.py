from django.core.management import BaseCommand

from barter_auth.models import BarterUser
from transactions.handlers import max_earnings_kitplan, total_earnings_kitplan, mark_cap_plans_as_reached


class Command(BaseCommand):
    help = 'Actualizar los registros cuyos planes ya fueron alcanzados'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        try:
            print('Iniciando actualización de planes alcanzados, obteniendo usuarios')
            users = BarterUser.objects.filter(plans__isnull=False).distinct()
            for user in users:
                print('Actualizando plan alcanzado de: ', user)

                # obtener el techo del usuario actual
                max_earning = max_earnings_kitplan(user)

                # obtener las ganancias actuales del usuario
                current_earnings = total_earnings_kitplan(user)

                # si las ganancias actuales son mayores o iguales al techo, entonces el techo fue alcanzado
                if current_earnings >= max_earning:
                    print(f'El techo de {user.username} fue alcanzado')
                    # actualizar el techo alcanzado de todos los planes activos
                    mark_cap_plans_as_reached(user)

        except Exception as e:
            print(e)
            raise e
