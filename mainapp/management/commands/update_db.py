from django.core.management.base import BaseCommand
# from django.contrib.auth.models import User
from authapp.models import ShopUser, ShopUserProfile

JSON_PATH = 'mainapp/json'


class Command(BaseCommand):
    def handle(self, *args, **options):
        users = ShopUser.objects.all()
        for user in users:
            user_profile = ShopUserProfile.objects.create(user=user)
            user_profile.save()
