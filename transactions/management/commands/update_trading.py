from django.core.management import BaseCommand
from django.db import transaction

from barter_auth.models import BarterTradingPlan
from global_settings.models import TradingPlans
from transactions.models import Transaction


class Command(BaseCommand):
    help = 'Actualizar los kit plan de los usuarios'

    @transaction.atomic()
    def handle(self, *args, **options):
        try:
            print('Iniciando actualización de plan de trading de los usuarios')

            plans = BarterTradingPlan.objects.filter(plan__isnull=True, transaction__isnull=True).distinct()
            print('Cantidad de planes a actualizar: ', len(plans))

            for plan in plans:
                print('Actualizando plan de trading de: ', plan.user, ' - ', plan.trading_amount)
                plan.plan = TradingPlans.objects.filter(price__gte=plan.trading_amount, enabled=True).order_by(
                    'price').first()
                plan.transaction = plan.user.transactions.filter(amount=plan.trading_amount, transaction_type='trading',
                                                                 trading_plans__isnull=True).first()
                plan.save()
                if plan.plan is None or plan.transaction is None:
                    print('No se pudo actualizar el plan de trading de: ', plan.user)
                    continue
                print('Plan actualizado: ', plan.plan, ' - ', plan.transaction.id)

            print('Transacciones sin plan')
            transactions = Transaction.objects.filter(transaction_type='trading', trading_plans__isnull=True)

            for transaction in transactions:
                print('Actualizando transacción: ', transaction)

                transaction.trading_plans.add(BarterTradingPlan.objects.create(
                    user=transaction.user,
                    trading_amount=transaction.amount,
                    transaction=transaction,
                    plan=TradingPlans.objects.filter(price__gte=transaction.amount, enabled=True).order_by(
                        'price').first(),
                    transaction_hash=transaction.transaction_hash
                ))
                transaction.save()
                print('Transacción actualizada: ', transaction.id)


        except Exception as e:
            print(e)
            raise e
