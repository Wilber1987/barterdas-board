from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from transactions.handlers import create_trading_earning_through_monthly_percentage
from transactions.models import MonthlyTradingEarnings


@receiver(pre_save, sender=MonthlyTradingEarnings)
def validator_for_duplicated_monthly_trading_earning_report(sender, instance: MonthlyTradingEarnings, **kwargs):
    if MonthlyTradingEarnings.objects.filter(month=instance.month, year=instance.year).first() and not instance.pk:
        raise Exception('Ya se ha generado el reporte de este mes')


@receiver(post_save, sender=MonthlyTradingEarnings)
def create_trading_earning_report_on_cut_off_date(sender, instance: MonthlyTradingEarnings, created,
                                                  **kwargs):  # Based on the monthly earnings, personal and network trading earnings will be calculated.
    if not created:  # Only when the Cut-off date is created, will the earnings be calculated.
        return
    create_trading_earning_through_monthly_percentage(instance)
