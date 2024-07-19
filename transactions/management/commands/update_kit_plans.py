from django.core.management import BaseCommand
from django.db import transaction

from barter_auth.models import BarterPlan
from global_settings.models import KitPlan
from transactions.models import Transaction


class Command(BaseCommand):
    help = 'Actualizar los kit plan de los usuarios'

    @transaction.atomic()
    def handle(self, *args, **options):
        try:
            print('Iniciando actualización de plan de trading de los usuarios')

            plans = BarterPlan.objects.filter(plan__isnull=True, transaction__isnull=True).distinct()
            print('Cantidad de planes a actualizar: ', len(plans))

            for plan in plans:
                print('Actualizando plan de kit plan de: ', plan.user, ' - ', plan.selected_plan)
                plan.plan = KitPlan.objects.filter(price__gte=plan.selected_plan, enabled=True).order_by(
                    'price').first()
                plan.transaction = plan.user.transactions.filter(
                    amount=plan.selected_plan,
                    transaction_type='kit-plan',
                    kit_plans__isnull=True
                ).first()
                plan.save()
                print('Plan actualizado: ', plan.plan, ' - ', plan.transaction)

            print('Transacciones sin plan')
            transactions = Transaction.objects.filter(transaction_type='kit-plan', kit_plans__isnull=True)

            for transaction in transactions:
                print('Actualizando transacción: ', transaction)

                transaction.kit_plans.add(BarterPlan.objects.create(
                    user=transaction.user,
                    selected_plan=transaction.amount,
                    transaction=transaction,
                    plan=KitPlan.objects.filter(price__gte=transaction.amount, enabled=True).order_by('price').first(),
                    transaction_hash=transaction.transaction_hash
                ))
                transaction.save()
                print('Transacción actualizada: ', transaction.kit_plans)


        except Exception as e:
            print(e)
            raise e
