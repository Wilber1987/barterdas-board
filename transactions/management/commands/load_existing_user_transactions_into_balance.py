from django.core.management import BaseCommand
from transactions.models import BalanceHistory, BalanceTransactionType, Transaction
from transactions.utils.balance_utils import (
    generate_transaction_balance_history_instances,
    save_balance_history,
)


class Command(BaseCommand):
    help = """Command to load existing transactions into a user's balance.
    Safe, can be executed multiple times without duplicating data."""

    def handle(self, *args, **kwargs):
        transaction_types_to_look = ["PTT", "PTK", "PTC"]

        transactions_already_registered_in_balance = BalanceHistory.objects.filter(
            balance_transaction_type__unique_code__in=transaction_types_to_look
        )

        transactions_pending = Transaction.objects.filter(
            transaction_status=1,
            wallet_deposit_date__isnull=False,
        ).exclude(
            wallet_deposit_date="",
            id__in=transactions_already_registered_in_balance.values_list(
                "object_id", flat=True
            ),
        )

        balance_history_to_create = []

        for transaction in transactions_pending:
            balance_history_to_create.extend(
                generate_transaction_balance_history_instances(transaction)
            )

        for balance_history in balance_history_to_create:
            save_balance_history(balance_history)
