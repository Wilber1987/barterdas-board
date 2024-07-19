import csv

from barter_auth.models import BarterUser, BarterUserNode, BarterPlan, BarterTradingPlan

from django.core.management import BaseCommand

from barter_auth.v2.utils import calculate_user_balance


class Command(BaseCommand):
    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        # Index for all users
        barter_plan_nulles = BarterPlan.objects.filter(transaction__isnull=True)
        barter_trading_nulles = BarterTradingPlan.objects.filter(transaction__isnull=True)

        # calcular todas los balances
        results = []
        for barter_plan in barter_plan_nulles:
            results.append(
                {'user_id': barter_plan.user.id, 'plan_id': barter_plan.id, 'plan_selected': barter_plan.selected_plan,
                 'type': 'plan'})

        for barter_trading in barter_trading_nulles:
            results.append(
                {'user_id': barter_trading.user.id, 'plan_selected': barter_trading.trading_amount, 'type': 'trading',
                 'plan_id': barter_trading.id})

        self.stdout.write(f'Se han afectado {len(results)} registros', style_func=self.style.SUCCESS)

        # guardando los resultados en un archivo
        campos = set()
        for diccionario in results:
            campos.update(obtener_valores(diccionario).keys())

        with open('huerfanos.csv', 'w', newline='') as archivo:
            escritor = csv.DictWriter(archivo, fieldnames=sorted(campos))

            escritor.writeheader()
            for diccionario in results:
                escritor.writerow(obtener_valores(diccionario))
        self.stdout.write(f'Archivo huerfanos.csv guardado', style_func=self.style.SUCCESS)


def obtener_valores(diccionario, prefijo=''):
    valores = {}
    for clave, valor in diccionario.items():
        if isinstance(valor, dict):
            valores.update(obtener_valores(valor, prefijo + clave + '_'))
        else:
            valores[prefijo + clave] = valor
    return valores
