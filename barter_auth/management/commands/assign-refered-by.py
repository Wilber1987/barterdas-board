from barter_auth.models import BarterUser, BarterUserNode

from django.core.management import BaseCommand

class Command(BaseCommand):
    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        # Index for count affected registers
        index = 0
        index_2 = 0

        for node in BarterUserNode.objects.all():
            user = node.investment
            if user.referred_by == None: # Save leader if user dont have one
                user.referred_by = node.user
                user.save()
                index = index+1
            else:
                index_2 = index_2+1
        self.stdout.write(f'Se han afectado {index} registros, {index_2} registros no se afectaron porque ya existia el referido', style_func = self.style.SUCCESS)