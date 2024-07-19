from transactions.models import Transaction
from transactions.handlers import generate_kitplan_unilevel_earnings

from django.core.management import BaseCommand

class Command(BaseCommand):
    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        transaction_list = Transaction.objects.filter(transaction_status=Transaction.TRANSACTION_STATUS[1][0], # Es Verificado
                                   transaction_type=Transaction.TRANSACTION_TYPE[0][0], calculated_earnings=False)     # Tipo Kit Plan

        for transaction in transaction_list:
            generate_kitplan_unilevel_earnings(transaction)

        print(f'Se ha completado el reporte de ganancias.')