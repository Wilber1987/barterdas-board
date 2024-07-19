from barter_auth.models import BarterUser
from barter_auth.helpers import add_user_to_network

from django.core.management import BaseCommand

class Command(BaseCommand):
    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        for user in BarterUser.objects.filter(referred_by__isnull=False):
            add_user_to_network(user)

        self.stdout.write('Si se pudo', style_func = self.style.SUCCESS)