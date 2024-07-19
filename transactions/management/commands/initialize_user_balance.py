from django.core.management import BaseCommand
from barter_auth.models import BarterUser
from transactions.models import Balance
from transactions.utils.balance_utils import generate_initial_balance_instance


class Command(BaseCommand):
    help = "Commad to generate initial instances of Balance for BarterUser instances that don't have it already"

    def handle(self, *args, **kwargs):
        users_without_balance = BarterUser.objects.exclude(
            pk__in=Balance.objects.values("user")
        )

        new_balance_instances = [
            generate_initial_balance_instance(user) for user in users_without_balance
        ]

        Balance.objects.bulk_create(new_balance_instances)

        print(f"Created {len(new_balance_instances)} new balance instances")