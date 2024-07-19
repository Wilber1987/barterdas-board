from decimal import Decimal
from django.dispatch import receiver
from django.db.models.signals import post_save

from transactions.models import ReInvestments
from transactions.handlers import get_renueve_trading_total, get_renueve_co_founder


@receiver(post_save, sender=ReInvestments)
def after_of_create_re_investments(sender, instance: ReInvestments, created, **kwargs):
    if not created:
        return

    amount = instance.amount
    user = instance.user

    if (
        instance.type_re_investment
        == ReInvestments.TYPE_RE_INVESTMENT[0][0]  # Trading reinvestment
    ):
        if instance.amount > get_renueve_trading_total(instance.user):
            return

        amount_paid = amount

        # Withdraw first from personal earnings
        for renueve in user.cumulative_revenues.all():
            if renueve.total_to_withdraw == 0:
                continue
            if renueve.total_to_withdraw >= amount_paid:
                renueve.total_to_withdraw -= amount_paid
                renueve.save()
                amount_paid = 0
                break
            else:
                amount_paid -= renueve.total_to_withdraw
                renueve.total_to_withdraw = 0
                renueve.save()

        # If there is still amount remaining to be paid, then debit from network earnings
        if amount_paid > 0:
            for renueve in user.monthly_trading_earnings.all():
                if renueve.earnings_paid >= renueve.earnings:
                    continue
                if renueve.earnings_paid + amount_paid <= renueve.earnings:
                    renueve.earnings_paid += amount_paid
                    renueve.save()
                    amount_paid = 0
                    break
                else:
                    amount_paid -= renueve.earnings - renueve.earnings_paid
                    renueve.earnings_paid = renueve.earnings
                    renueve.save()

        # If there is still amount remaining to be paid, update amount
        if amount_paid > 0:
            instance.amount = amount_paid
            instance.save()

    elif (
        instance.type_re_investment
        == ReInvestments.TYPE_RE_INVESTMENT[1][0]  # Cofounder reinvestment
    ):
        if instance.amount > get_renueve_co_founder(instance.user):
            raise Exception("No tiene el dinero suficiente para reinvertir")

        amount_paid = amount

        # Withdraw first from cofounder trading earnings
        for renueve in user.co_founder_earning_by_trading.all():
            if renueve.earnings_paid >= renueve.earnings:
                continue
            if renueve.earnings_paid + amount_paid <= renueve.earnings:
                renueve.earnings_paid += amount_paid
                renueve.save()
                amount_paid = 0
                break
            else:
                amount_paid -= renueve.earnings - renueve.earnings_paid
                renueve.earnings_paid = renueve.earnings
                renueve.save()

        # If there is still amount remaining to be paid, withdraw from cofounder product earnings
        if amount_paid > 0:
            for renueve in user.co_founder_earning_by_products.all():
                if renueve.earnings_paid >= renueve.earnings:
                    continue
                if renueve.earnings_paid + amount_paid <= renueve.earnings:
                    renueve.earnings_paid += amount_paid
                    renueve.save()
                    amount_paid = 0
                    break
                else:
                    amount_paid -= renueve.earnings - renueve.earnings_paid
                    renueve.earnings_paid = renueve.earnings
                    renueve.save()

        # If there is still amount remaining to be paid, update amount
        if amount_paid > 0:
            instance.amount = amount_paid
            instance.save()
    else:
        raise Exception("Tipo de reinversión no válido")
