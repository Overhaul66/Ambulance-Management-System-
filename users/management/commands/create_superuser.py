from django.core.management.base import BaseCommand
from users.models import CustomUser

class Command(BaseCommand):
    help = 'Create a superuser with a phone number or email'

    def add_arguments(self, parser):
        parser.add_argument('--phone_number', type=str, help='Phone number of the superuser')
        parser.add_argument('--email', type=str, help='Email of the superuser')
        parser.add_argument('--password', type=str, help='Password for the superuser')

    def handle(self, *args, **options):
        phone_number = options['phone_number']
        email = options['email']
        password = options['password']

        if not phone_number and not email:
            self.stdout.write(self.style.ERROR('You must provide either a phone number or an email.'))
            return

        if not password:
            self.stdout.write(self.style.ERROR('You must provide a password.'))
            return

        user = CustomUser.objects.create_superuser(phone_number=phone_number, email=email, password=password)
        self.stdout.write(self.style.SUCCESS(f'Superuser created: {user.phone_number or user.email}'))
