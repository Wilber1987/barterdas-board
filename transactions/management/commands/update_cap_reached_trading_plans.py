from django.core.management import BaseCommand

from barter_auth.models import BarterUser
from transactions.handlers import get_max_trading_earnings, get_current_trading_earnings, \
    mark_cap_trading_plans_as_reached


class Command(BaseCommand):
    help = 'Actualizar los registros cuyos planes ya fueron alcanzados'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        try:
            print('Iniciando actualización de planes alcanzados, obteniendo usuarios')
            users = BarterUser.objects.filter(bartertradingplan__isnull=False).distinct()
            for user in users:
                print('Actualizando plan alcanzado de: ', user)

                # obtener el techo del usuario actual
                max_earning = get_max_trading_earnings(user)

                # obtener las ganancias actuales del usuario
                current_earnings = get_current_trading_earnings(user)

                # si las ganancias actuales son mayores o iguales al techo, entonces el techo fue alcanzado
                if current_earnings >= max_earning:
                    print(f'El techo de {user.username} fue alcanzado')
                    # actualizar el techo alcanzado de todos los planes activos
                    mark_cap_trading_plans_as_reached(user)

        except Exception as e:
            print(e)
            raise e
