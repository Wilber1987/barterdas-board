import csv

from django.core.management import BaseCommand

from barter_auth.models import BarterUser


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('file', nargs='+', type=str)

    def handle(self, *args, **options):
        file = options['file'][0]
        print(file)
        with open(file, 'r') as users:
            reader = csv.DictReader(users, delimiter=';')
            marked = 0

            for user in reader:
                try:
                    record = BarterUser.objects.get(email=user['email'])
                    record.is_co_founder = True
                    record.save()
                    marked += 1
                except Exception as e:
                    print(e)

            self.stdout.write(self.style.SUCCESS(f'{marked} users marked as co-founders'))