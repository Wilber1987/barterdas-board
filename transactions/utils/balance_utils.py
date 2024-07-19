import logging

from django.db import transaction

from transactions.models import (
    Balance,
    BalanceHistory,
    BalanceTransactionType,
    Transaction,
)

logger = logging.getLogger("django")


def generate_initial_balance_instance(user) -> Balance:
    """Returns an user's initial balance instance to be saved or bulk_created"""

    return Balance(
        user=user,
        general_balance=0,
        cofounder_balance=0,
        cofounder_earnings=0,
        trading_balance=0,
        trading_earnings=0,
        trading_network_earnings=0,
        kitplan_balance=0,
        kitplan_network_earnings=0,
        enabled=True,
    )