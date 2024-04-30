from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        user = User.objects.create(
            email='test@ya.ru',
            is_superuser=True,
            is_active=True,
            is_staff=True
        )
        user.set_password('1234567')
        user.save()
