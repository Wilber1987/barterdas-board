from transactions.models import TradingEarnings
from transactions.handlers import create_trading_earning_through_monthly_percentage_with_network

from django.dispatch import receiver
from django.db.models.signals import  post_save


@receiver(post_save, sender=TradingEarnings)
def create_network_trading_earning_on_personal_trading_earnings(sender, instance: TradingEarnings, created, **kwargs):
    if not created:
        return
    if instance.calculated_earnings:
        return
    create_trading_earning_through_monthly_percentage_with_network(instance)
    instance.calculated_earnings = True
    instance.save()