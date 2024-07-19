import calendar
import datetime

import pytz
from django.db.models import Sum

from transactions.models import (
    Transaction,
    ReInvestments,
    Withdrawal,
    DetailCoFounderEarningByTrading,
    DetailCoFounderEarningByProducts,
    UserDailyTradingRevenue, MonthlyTradingEarningsPerLeader,
    KitPlanNetWorkEarnings, TradingNetWorkEarnings, TradingEarnings,
)


def calculate_user_balance(user):
    user_balance = {
        'trading': {
            'balance': 0,
            'current_earnings': 0,
            'current_network_earnings': 0,
            'balance_pending_approval': 0
        },
        'kitplan': {
            'balance': 0,
            'current_network_earnings': 0,
            'balance_pending_approval': 0
        },
        'cofounder': {
            'balance': 0,
            'current_earnings': 0,
            'balance_pending_approval': 0
        },
        'total_monthly_earnings': {
            'balance': 0
        }
    }

    # region previous model data for first users
    # Do not modify this unless the previous model
    # data has been sent to the new models
    # or you are going to have a bad time
    # -jeff

    previous_model_trading_data = UserDailyTradingRevenue.objects.filter(
        user=user,
    ).aggregate(Sum('earnings'))['earnings__sum']

    if previous_model_trading_data:
        user_balance['trading']['current_earnings'] += previous_model_trading_data

    previous_model_trading_network_data = MonthlyTradingEarningsPerLeader.objects.filter(
        user=user
    ).aggregate(Sum('earnings'))['earnings__sum']

    if previous_model_trading_network_data:
        user_balance['trading']['current_network_earnings'] += previous_model_trading_network_data
    # endregion

    # region get cofounder data
    approved_cofounder_balance = Transaction.objects.filter(
        user=user,
        description__icontains='initial',
        transaction_status=1
    ).aggregate(Sum('amount'))['amount__sum']

    cofounder_balance_pending_approval = Transaction.objects.filter(
        user=user,
        description__icontains='initial',
        transaction_status=0
    ).aggregate(Sum('amount'))['amount__sum']

    cofounder_earnings_by_trading = DetailCoFounderEarningByTrading.objects.filter(
        user=user
    ).aggregate(Sum('earnings'))['earnings__sum']

    cofounder_earnings_by_product = DetailCoFounderEarningByProducts.objects.filter(
        user=user
    ).aggregate(Sum('earnings'))['earnings__sum']

    cofounder_reinvestments = ReInvestments.objects.filter(
        user=user,
        type_re_investment='Co-Founder'
    ).aggregate(Sum('amount'))['amount__sum']

    cofounder_earnings_withdrawals = Withdrawal.objects.filter(
        user=user,
        source_of_profit='CO_FOUNDER',
        transaction_status=1
    ).aggregate(Sum('amount'))['amount__sum']

    if approved_cofounder_balance:
        user_balance['cofounder']['balance'] += approved_cofounder_balance
    if cofounder_balance_pending_approval:
        user_balance['cofounder']['balance_pending_approval'] += cofounder_balance_pending_approval
    if cofounder_earnings_by_trading:
        user_balance['cofounder']['current_earnings'] += cofounder_earnings_by_trading
    if cofounder_earnings_by_product:
        user_balance['cofounder']['current_earnings'] += cofounder_earnings_by_product
    if cofounder_earnings_withdrawals:
        user_balance['cofounder']['current_earnings'] -= cofounder_earnings_withdrawals
    if cofounder_reinvestments:
        user_balance['cofounder']['balance'] += cofounder_reinvestments
        user_balance['cofounder']['current_earnings'] -= cofounder_reinvestments
    # endregion

    # region get trading data
    approved_trading_balance = Transaction.objects.filter(
        user=user,
        description__icontains='trading',
        transaction_status=1
    ).aggregate(Sum('amount'))['amount__sum']

    trading_balance_pending_approval = Transaction.objects.filter(
        user=user,
        description__icontains='trading',
        transaction_status=0
    ).aggregate(Sum('amount'))['amount__sum']

    trading_reinvestments = ReInvestments.objects.filter(
        user=user,
        type_re_investment='Trading'
    ).aggregate(Sum('amount'))['amount__sum']

    trading_earnings_withdrawals = Withdrawal.objects.filter(
        user=user,
        source_of_profit='TRADING',
        transaction_status=1
    ).aggregate(Sum('amount'))['amount__sum']

    trading_personal_earnings = TradingEarnings.objects.filter(
        user=user
    ).aggregate(Sum('earnings'))['earnings__sum']

    if trading_personal_earnings:
        user_balance['trading']['current_earnings'] += trading_personal_earnings
    if approved_trading_balance:
        user_balance['trading']['balance'] += approved_trading_balance
    if trading_balance_pending_approval:
        user_balance['trading']['balance_pending_approval'] += trading_balance_pending_approval
    if trading_reinvestments:
        user_balance['trading']['balance'] += trading_reinvestments
        user_balance['trading']['current_earnings'] -= trading_reinvestments
    if trading_earnings_withdrawals:
        user_balance['trading']['current_earnings'] -= trading_earnings_withdrawals

    trading_network_earnings = TradingNetWorkEarnings.objects.filter(
        unilevel_network__user=user
    ).aggregate(Sum('earnings'))['earnings__sum']
    # si no hay ganancias de la red, se asigna 0
    trading_network_earnings = trading_network_earnings if trading_network_earnings else 0

    # se calcula el balance actual de ganancias de la red
    if user_balance['trading']['current_earnings'] > 0:
        user_balance['trading']['current_network_earnings'] += trading_network_earnings
    else:
        user_balance['trading']['current_network_earnings'] += trading_network_earnings + user_balance['trading']['current_earnings']
        user_balance['trading']['current_earnings'] = 0

        if user_balance['trading']['current_network_earnings'] < 0:
            user_balance['trading']['current_network_earnings'] = 0

    # endregion

    # region get kitplan data
    kitplan_transactions = Transaction.objects.filter(
        user=user,
        description__icontains='kit'
    ).exclude(transaction_status=2)

    # obtener el total de ganancias de la red
    kitplan_network_earnings = KitPlanNetWorkEarnings.objects.filter(
        unilevel_network__user=user
    ).aggregate(Sum('earnings'))['earnings__sum']
    # si no hay ganancias de la red, se asigna 0
    kitplan_network_earnings = kitplan_network_earnings if kitplan_network_earnings else 0

    # obtener el total de retiros de ganancias de la red verificados
    kitplan_earnings_withdrawals = Withdrawal.objects.filter(
        user=user,
        source_of_profit='KIT_PLAN',
        transaction_status=1
    ).aggregate(Sum('amount'))['amount__sum']

    # si no hay retiros de ganancias de la red, se asigna 0
    kitplan_earnings_withdrawals = kitplan_earnings_withdrawals if kitplan_earnings_withdrawals else 0

    # se calcula el balance actual de ganancias de la red
    user_balance['kitplan']['current_network_earnings'] = kitplan_network_earnings - kitplan_earnings_withdrawals

    if kitplan_transactions:
        for transaction in kitplan_transactions:
            if transaction.transaction_status == 1:
                user_balance['kitplan']['balance'] += transaction.amount
            else:
                user_balance['kitplan']['balance_pending_approval'] += transaction.amount
    # endregion

    return user_balance


def get_month_dates(month, year):
    """
    Dado un mes y un año, retorna la fecha del primer día del mes y la fecha del último día del mes
    También retorna el número de días del mes dado
    @param month: mes
    @param year: año
    @return: fecha del primer día del mes, fecha del último día del mes, número de días del mes
    """
    utc = pytz.UTC
    date_first_day = datetime.datetime(year, month, 1)
    last_day = calendar.monthrange(date_first_day.year, date_first_day.month)[1]
    date_last_day = datetime.datetime(date_first_day.year, date_first_day.month, last_day)
    date_first_day = utc.localize(date_first_day)
    date_last_day = utc.localize(date_last_day)
    return date_first_day, date_last_day, last_day
