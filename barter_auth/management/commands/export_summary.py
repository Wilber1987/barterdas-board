import csv

from barter_auth.models import BarterUser, BarterUserNode

from django.core.management import BaseCommand

from barter_auth.v2.utils import calculate_user_balance


class Command(BaseCommand):
    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        # Index for all users
        users = BarterUser.objects.all()

        # calcular todas los balances
        results = []
        for user in users:
            results.append(calculate_user_balance(user))
            self.stdout.write(f'Se ha calculado el balance de {user.email}', style_func=self.style.SUCCESS)

        self.stdout.write(f'Se han afectado {len(results)} registros', style_func=self.style.SUCCESS)

        # guardando los resultados en un archivo
        campos = set()
        for diccionario in results:
            campos.update(obtener_valores(diccionario).keys())

        self.stdout.write(f'Campos: {campos}', style_func=self.style.SUCCESS)
        self.stdout.write(f'Campos ordenados: {sorted(campos)}', style_func=self.style.SUCCESS)
        self.stdout.write(f'Guardando en archivo balances.csv', style_func=self.style.SUCCESS)
        with open('balances-prod-2.csv', 'w', newline='') as archivo:
            escritor = csv.DictWriter(archivo, fieldnames=sorted(campos))

            escritor.writeheader()
            for diccionario in results:
                escritor.writerow(obtener_valores(diccionario))
        self.stdout.write(f'Archivo balances.csv guardado', style_func=self.style.SUCCESS)


def obtener_valores(diccionario, prefijo=''):
    valores = {}
    for clave, valor in diccionario.items():
        if isinstance(valor, dict):
            valores.update(obtener_valores(valor, prefijo + clave + '_'))
        else:
            valores[prefijo + clave] = valor
    return valores
