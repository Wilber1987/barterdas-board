from django.core.management import BaseCommand
from django.db import transaction

from barter_auth.models import Referral, BarterUserNode
from transactions.models import Transaction


class Command(BaseCommand):
    help = 'Migrate users and genealogy to new schema'

    @transaction.atomic()
    def handle(self, *args, **options):
        try:
            referrals = Referral.objects.all()

            for referral in referrals:
                node = BarterUserNode.objects.create(user=referral.user, investment=referral.investment,
                                                     category=referral.category)
                node.save()

                node_transaction = Transaction.objects.create(
                    user=referral.investment,
                    transaction_hash=referral.transaction_hash,
                    description='Initial investment',
                    amount=referral.amount or 0.0,
                    transaction_status=0
                )
                node_transaction.save()
            self.stdout.write(self.style.SUCCESS('Migrated referrals to new table!'))
        except Exception as e:
            print(e)
