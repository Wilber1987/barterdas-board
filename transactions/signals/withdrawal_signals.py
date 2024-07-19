from transactions.models import Withdrawal

from django.dispatch import receiver
from django.db.models.signals import post_save


@receiver(post_save, sender=Withdrawal)
def calculated_fields_for_created_records_of_withdrawals(sender, instance: Withdrawal, created, **kwargs):
    if not created:
        return
    if not instance.amount:
        return
    instance.fee_amount = float(instance.amount) * 0.04
    instance.amount_after_fee = float(instance.amount) - float(instance.fee_amount)
    instance.save()