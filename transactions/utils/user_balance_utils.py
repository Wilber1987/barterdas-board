from decimal import Decimal
from typing import Tuple

from django.db.models import Sum

from transactions.models import (
    DetailCoFounderEarningByProducts,
    DetailCoFounderEarningByTrading,
    KitPlanNetWorkEarnings,
    MonthlyTradingEarningsPerLeader,
    ReInvestments,
    TradingEarnings,
    TradingNetWorkEarnings,
    Transaction,
    UserDailyTradingRevenue,
    Withdrawal,
)


def get_user_current_trading_balance(user) -> Decimal:
    trading_balance = Decimal(0)

    transactions_queryset = Transaction.objects.filter(
        user=user, transaction_status=1, transaction_type="trading"
    )

    if transactions_queryset.exists():
        trading_balance_data = transactions_queryset.aggregate(Sum("amount"))[
            "amount__sum"
        ]

        trading_balance += trading_balance_data

    reinvestments_queryset = ReInvestments.objects.filter(
        user=user, type_re_investment="Trading"
    )

    if reinvestments_queryset.exists():
        reinvestments_data = reinvestments_queryset.aggregate(Sum("amount"))[
            "amount__sum"
        ]

        trading_balance += reinvestments_data

    return Decimal(trading_balance)


def get_user_current_trading_earnings(user) -> Tuple[Decimal, Decimal, Decimal]:
    personal_trading_earnings = Decimal(0)
    network_trading_earnings = Decimal(0)
    total_earnings = Decimal(0)

    user_daily_trading_revenue_queryset = UserDailyTradingRevenue.objects.filter(
        user=user
    )

    if user_daily_trading_revenue_queryset.exists():
        old_personal_trading_earnings_data = (
            user_daily_trading_revenue_queryset.aggregate(Sum("earnings"))[
                "earnings__sum"
            ]
        )

        personal_trading_earnings += Decimal(
            f"{old_personal_trading_earnings_data:.2f}"
        )

    trading_earnings_queryset = TradingEarnings.objects.filter(user=user)

    if trading_earnings_queryset.exists():
        personal_trading_earnings_data = trading_earnings_queryset.aggregate(
            Sum("earnings")
        )["earnings__sum"]

        personal_trading_earnings += Decimal(f"{personal_trading_earnings_data:.2f}")

    withdrawal_queryset = Withdrawal.objects.filter(
        user=user, source_of_profit="TRADING", transaction_status=1
    )

    if withdrawal_queryset.exists():
        withdrawal_data = withdrawal_queryset.aggregate(Sum("amount"))["amount__sum"]

        personal_trading_earnings -= Decimal(f"{withdrawal_data:.2f}")

    reinvestments_queryset = ReInvestments.objects.filter(
        user=user, type_re_investment="Trading"
    )

    if reinvestments_queryset.exists():
        reinvestments_data = reinvestments_queryset.aggregate(Sum("amount"))[
            "amount__sum"
        ]

        personal_trading_earnings -= Decimal(f"{reinvestments_data:.2f}")

    monthly_trading_earnings_per_leader_queryset = (
        MonthlyTradingEarningsPerLeader.objects.filter(user=user)
    )

    if monthly_trading_earnings_per_leader_queryset.exists():
        old_trading_network_earnings_data = (
            monthly_trading_earnings_per_leader_queryset.aggregate(Sum("earnings"))[
                "earnings__sum"
            ]
        )

        network_trading_earnings += Decimal(f"{old_trading_network_earnings_data:.2f}")

    trading_network_earnings_queryset = TradingNetWorkEarnings.objects.filter(
        unilevel_network__user=user
    )

    if trading_network_earnings_queryset.exists():
        trading_network_earnings_data = trading_network_earnings_queryset.aggregate(
            Sum("earnings")
        )["earnings__sum"]

        network_trading_earnings += Decimal(f"{trading_network_earnings_data:.2f}")

    if personal_trading_earnings < 0:
        network_trading_earnings += personal_trading_earnings
        personal_trading_earnings = 0

    total_earnings = personal_trading_earnings + network_trading_earnings

    return personal_trading_earnings, network_trading_earnings, total_earnings


def get_user_current_kitplan_balance(user) -> Decimal:
    kitplan_balance = 0

    transactions_queryset = Transaction.objects.filter(
        user=user, transaction_type="kit-plan", transaction_status=1
    )

    if transactions_queryset.exists():
        kitplan_data = transactions_queryset.aggregate(Sum("amount"))["amount__sum"]

        kitplan_balance += Decimal(f"{kitplan_data:.2f}")

    return kitplan_balance


def get_user_current_kitplan_earnings(user) -> Decimal:
    kitplan_earnings = Decimal(0)

    kitplan_earnings_queryset = KitPlanNetWorkEarnings.objects.filter(
        unilevel_network__user=user
    )

    if kitplan_earnings_queryset.exists():
        kitplan_earnings_data = kitplan_earnings_queryset.aggregate(Sum("earnings"))[
            "earnings__sum"
        ]

        kitplan_earnings += Decimal(f"{kitplan_earnings_data:.2f}")

    kitplan_withdrawals_queryset = Withdrawal.objects.filter(
        user=user, source_of_profit="KIT_PLAN", transaction_status=1
    )

    if kitplan_withdrawals_queryset.exists():
        kitplan_withdrawals_data = kitplan_withdrawals_queryset.aggregate(
            Sum("amount")
        )["amount__sum"]

        kitplan_earnings -= Decimal(f"{kitplan_withdrawals_data:.2f}")

    return kitplan_earnings


def get_user_current_cofounder_balance(user) -> Decimal:
    cofounder_balance = Decimal(0)

    cofounder_transaction_queryset = Transaction.objects.filter(
        user=user, transaction_status=1, transaction_type="co-founder"
    )

    if cofounder_transaction_queryset.exists():
        cofounder_balance_data = cofounder_transaction_queryset.aggregate(
            Sum("amount")
        )["amount__sum"]

        cofounder_balance += Decimal(f"{cofounder_balance_data:.2f}")

    cofounder_reinvestments_queryset = ReInvestments.objects.filter(
        user=user, type_re_investment="Co-Founder"
    )

    if cofounder_reinvestments_queryset.exists():
        cofounder_reinvestments_data = cofounder_reinvestments_queryset.aggregate(
            Sum("amount")
        )["amount__sum"]

        cofounder_balance += Decimal(f"{cofounder_reinvestments_data:.2f}")

    return cofounder_balance


def get_user_current_cofounder_earnings(user) -> Tuple[Decimal, Decimal, Decimal]:
    cofounder_earnings_by_product = Decimal(0)
    cofounder_earnings_by_trading = Decimal(0)
    total_cofounder_earnings = Decimal(0)

    cofounder_earnings_product_queryset = (
        DetailCoFounderEarningByProducts.objects.filter(user=user)
    )

    if cofounder_earnings_product_queryset.exists():
        product_earnings_data = cofounder_earnings_product_queryset.aggregate(
            Sum("earnings")
        )["earnings__sum"]

        cofounder_earnings_by_product += Decimal(f"{product_earnings_data:.2f}")

    cofounder_earning_by_trading_queryset = (
        DetailCoFounderEarningByTrading.objects.filter(user=user)
    )

    if cofounder_earning_by_trading_queryset.exists():
        trading_earnings_data = cofounder_earning_by_trading_queryset.aggregate(
            Sum("earnings")
        )["earnings__sum"]

        cofounder_earnings_by_trading += Decimal(f"{trading_earnings_data:.2f}")

    cofounder_reinvestments_queryset = ReInvestments.objects.filter(
        user=user, type_re_investment="Co-Founder"
    )

    if cofounder_reinvestments_queryset.exists():
        cofounder_reinvestments_data = cofounder_reinvestments_queryset.aggregate(
            Sum("amount")
        )["amount__sum"]

        cofounder_earnings_by_product -= Decimal(f"{cofounder_reinvestments_data:.2f}")

    cofounder_withdrawals_queryset = Withdrawal.objects.filter(
        user=user, source_of_profit="CO_FOUNDER", transaction_status=1
    )

    if cofounder_withdrawals_queryset.exists():
        cofounder_withdrawals_data = cofounder_withdrawals_queryset.aggregate(
            Sum("amount")
        )["amount__sum"]

        cofounder_earnings_by_product -= Decimal(f"{cofounder_withdrawals_data:.2f}")

    if cofounder_earnings_by_product < 0:
        cofounder_earnings_by_trading += cofounder_earnings_by_product
        cofounder_earnings_by_product = 0

        if cofounder_earnings_by_trading < 0:
            cofounder_earnings_by_trading = 0

    total_cofounder_earnings = (
        cofounder_earnings_by_product + cofounder_earnings_by_trading
    )

    return (
        cofounder_earnings_by_product,
        cofounder_earnings_by_trading,
        total_cofounder_earnings,
    )


def get_count_users_direct(user):
    status_verified = Transaction.TRANSACTION_STATUS[1][0]
    # se obtiene todos los usuarios directos que han hecho una transacción verificada
    count = (
        user.unilevel_network.filter(
            level=1,
            user_in_network__transactions__transaction_status=status_verified,
        )
        .distinct()
        .count()
    )
    return count
