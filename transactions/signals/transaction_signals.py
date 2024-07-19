"""All of transactions signals"""

from django.db.models.signals import post_save
from django.dispatch import receiver

from barter_auth.models import BarterUser
from transactions.models import Transaction, KitPlanNetWorkEarnings
from transactions.handlers import create_kit_plan_earning_through_transactions
from sales_funnel.models import SalesFunnelOwner


@receiver(post_save, sender=Transaction)
def create_or_enable_salesfunnelowner(sender, instance: Transaction, created, **kwargs):
    if (
        instance.transaction_status != Transaction.TRANSACTION_STATUS[1][0]
        or instance.transaction_type != Transaction.TRANSACTION_TYPE[0][0]
    ):
        return

    if instance.amount < 50:
        return

    user = instance.user

    if user.sales_funnel.count() > 0:
        funnel = user.sales_funnel.first()

        if not funnel.enabled:
            funnel.enabled = True
            funnel.save()
    else:
        SalesFunnelOwner.objects.create(
            user=user,
            username=user.email.replace(".", "-").split("@")[0] + f"-{user.id}",
            display_name=f"{user.first_name} {user.last_name}",
            email=user.email,
        )


@receiver(post_save, sender=Transaction)
def after_of_create_transaction(sender, instance: Transaction, created, **kwargs):
    if created:
        return

    if (
        instance.transaction_status == Transaction.TRANSACTION_STATUS[1][0]
        and instance.transaction_type == Transaction.TRANSACTION_TYPE[0][0]
    ):
        # si es un kit plan con status aprobado, se debe crear el registro
        if KitPlanNetWorkEarnings.objects.filter(transaction=instance).exists():
            print(
                f"El detalle de plan de ganancia para la transacción {instance} ya existe"
            )
            return

        # obtener usuario lider
        user_of_transaction: BarterUser = instance.user
        leaders = user_of_transaction.unilevel_network_in.all()

        if not leaders and not instance.calculated_earnings:
            instance.calculated_earnings = True
            instance.save()
            return

        for leader in leaders:
            create_kit_plan_earning_through_transactions(instance, leader)

    if (
        instance.transaction_status == Transaction.TRANSACTION_STATUS[1][0]
        and not instance.calculated_earnings
    ):
        instance.calculated_earnings = True
        instance.save()
