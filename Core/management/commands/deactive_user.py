from argparse import ArgumentParser

from django.core.management import BaseCommand, CommandError

from Core.models import User


class Command(BaseCommand):

    def add_arguments(self, parser: ArgumentParser):
        parser.add_argument('phone', metavar='PHONE', help="Activate specific User")

    def handle(self, *args, **options):
        phone = options['phone']
        try:
            user = User.objects.get(phone=phone)
            user.is_active = False
            user.save()
        except Exception as e:
            raise CommandError(e)

        print("User ("+self.style.WARNING(user)+") deactivated done")
