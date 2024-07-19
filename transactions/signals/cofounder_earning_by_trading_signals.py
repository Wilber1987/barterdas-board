"""All of CoFounderEarningByTrading model signals"""

import calendar
import datetime
from pytz import utc

from django.db.models import Sum
from django.db.models.signals import post_save
from django.dispatch import receiver
from decimal import Decimal

from barter_auth.models import BarterUser
from transactions.models import (
    Transaction,
    ReInvestments,
    CoFounderEarningByTrading,
    DetailCoFounderEarningByTrading,
)


@receiver(post_save, sender=CoFounderEarningByTrading)
def after_of_create_co_founder_earning_by_trading(sender, instance, created, **kwargs):
    if not created:
        return

    if not instance.trimester:
        instance.trimester = instance.month // 3 + 1
        instance.save()

    users = BarterUser.objects.filter(
        leadership_pool_type=instance.leadership_pool_type
    ).all()

    date_first_day = utc.localize(datetime.datetime(instance.year, instance.month, 1))

    last_day = calendar.monthrange(instance.year, instance.month)[1]
    date_last_day = utc.localize(
        datetime.datetime(instance.year, instance.month, last_day)
    )

    to_create = []

    for user in users:
        object_to_create = DetailCoFounderEarningByTrading()
        object_to_create.user = user
        description = ""
        earning = 0

        # region Previous trimester cofounder transactions

        # Verified transactions made in the previous trimester
        transactions = user.transactions.filter(
            transaction_status=Transaction.TRANSACTION_STATUS[1][0],
            transaction_type=Transaction.TRANSACTION_TYPE[2][0],
            wallet_deposit_date__lt=date_first_day,
        ).all()

        if transactions.count() > 0:
            total_transactions_amount = transactions.aggregate(Sum("amount"))[
                "amount__sum"
            ]

            earning = total_transactions_amount * Decimal(instance.earning_percentage)
            description = f"Pagando a: {user.username} - {total_transactions_amount} - {instance.earning_percentage}\n"
        # endregion

        # region Current month cofounder transactions

        # Verified transactions made in the current month are prorated
        transactions_current_month = user.transactions.filter(
            transaction_status=Transaction.TRANSACTION_STATUS[1][0],
            transaction_type=Transaction.TRANSACTION_TYPE[2][0],
            wallet_deposit_date__gte=date_first_day,
            wallet_deposit_date__lte=date_last_day,
        ).all()

        for transaction in transactions_current_month:
            count_days = (transaction.wallet_deposit_date - date_first_day).days
            percentage_to_pay = Decimal(1 - (count_days / last_day))

            earning_to_pay = (
                transaction.amount * percentage_to_pay * instance.earning_percentage
            )
            earning += earning_to_pay

            description += f"""Transacción: {transaction.amount} - {transaction.wallet_deposit_date}
            Porcentaje a pagar: {percentage_to_pay} - {count_days} - {last_day}
            "Ganancia a pagar: {earning_to_pay}
            """
        # endregion

        # region Previous trimester cofounder reinvestments

        # Verified cofounder reinvestments made in the last trimester
        re_investments = user.re_investments.filter(
            type_re_investment=ReInvestments.TYPE_RE_INVESTMENT[1][0],
            created_at__lt=date_first_day,
        ).all()

        if re_investments.count() > 0:
            total_re_investments_amount = re_investments.aggregate(Sum("amount"))[
                "amount__sum"
            ]

            earning += total_re_investments_amount * instance.earning_percentage

            description += f"Reinversiones: {total_re_investments_amount} - {instance.earning_percentage}\n"
        # endregion

        # region Current month cofounder reinvestments

        # Verified cofounder reinvestments made in the current month are prorated
        re_investments_current_month = user.re_investments.filter(
            type_re_investment=ReInvestments.TYPE_RE_INVESTMENT[1][0],
            created_at__gte=date_first_day,
            created_at__lte=date_last_day,
        ).all()

        for re_investment in re_investments_current_month:
            count_days = (re_investment.created_at - date_first_day).days
            percentage_to_pay = Decimal(1 - (count_days / last_day))

            earning_to_pay = (
                re_investment.amount * percentage_to_pay * instance.earning_percentage
            )
            earning += earning_to_pay

            description += f"""Reinversiones: {re_investment.amount} - {re_investment.created_at}
            Porcentaje a pagar: {percentage_to_pay} - {count_days} - {last_day}
            Porcentaje a pagar: {percentage_to_pay} - {count_days} - {last_day}
            """
        # endregion

        object_to_create.earnings = earning
        object_to_create.co_founder_earning_by_trading = instance
        object_to_create.earnings_paid = 0
        object_to_create.process = description

        if earning > 0:
            to_create.append(object_to_create)

        if instance.earning_percentage == 0 and (
            transactions.count() > 0 or transactions_current_month.count() > 0
        ):
            to_create.append(object_to_create)

    DetailCoFounderEarningByTrading.objects.bulk_create(to_create)
