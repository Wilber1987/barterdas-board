from django.core.management import BaseCommand
from django.db import transaction

from barter_auth.models import BarterUser
from transactions.handlers import create_kit_plan_earning_through_transactions
from transactions.models import Transaction


class Command(BaseCommand):
    help = 'Actualizar el plan de ganancias de los usuarios'

    @transaction.atomic()
    def handle(self, *args, **options):
        try:
            print('Iniciando actualización de plan de ganancias')
            users = BarterUser.objects.all()
            for user in users:
                print('Actualizando plan de ganancias de: ', user)
                # obtener todos los referidos de ese usuario
                user_nodes = user.unilevel_network.all()
                if len(user_nodes) == 0:
                    print(f'{user.username} no tiene referidos')
                    continue
                # filtrar solo aquellos que tienen un plan activo y aprobado
                active_nodes = user_nodes.filter(
                    user_in_network__transactions__transaction_type=Transaction.TRANSACTION_TYPE[0][0],  # kit plan
                    user_in_network__transactions__transaction_status=Transaction.TRANSACTION_STATUS[1][0]  # aprobado
                ).distinct()
                print('Cantidad de referidos con plan activo: ', len(active_nodes))

                if len(active_nodes) == 0:
                    print(f'{user.username} no tiene referidos con plan activo')
                    continue
                # por cada nodo activo, obtener la ganancia, insertar en el detalle y sumar a la ganancia total
                for node in active_nodes:
                    # obtener lsa transacciones de los kitplans por cada usuario en la red
                    total_invested = node.user_in_network.transactions.filter(
                        transaction_type=Transaction.TRANSACTION_TYPE[0][0],  # kit plan
                        transaction_status=Transaction.TRANSACTION_STATUS[1][0],  # aprobado
                        wallet_deposit_date__isnull=False)

                    # obtener el total invertido
                    for transaction_item in total_invested:
                        create_kit_plan_earning_through_transactions(transaction_item, node)

            pass
        except Exception as e:
            print(e)
            raise e
