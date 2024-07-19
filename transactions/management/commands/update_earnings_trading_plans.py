from django.core.management import BaseCommand
from django.db import transaction

from transactions.handlers import create_trading_earning_through_monthly_percentage
from transactions.models import MonthlyTradingEarnings


class Command(BaseCommand):
    help = 'Actualizar el plan de trading de ganancias de los usuarios'

    @transaction.atomic()
    def handle(self, *args, **options):
        try:
            print('Iniciando actualización de plan de ganancias')
            months = MonthlyTradingEarnings.objects.filter(month__gte=6)
            for month in months:
                create_trading_earning_through_monthly_percentage(month)

            pass
        except Exception as e:
            print(e)
            raise e
