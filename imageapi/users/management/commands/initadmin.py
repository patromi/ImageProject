import os

from django.conf import settings
from django.core.management import BaseCommand
from django.core.management.utils import get_random_secret_key
from users.models import ImageUser as User

class Command(BaseCommand):

    def handle(self, *args, **options):
        if User.objects.count() == 0:
            email = 'admin@gmail.com'
            password = 'admin'
            print('Creating account for %s ' % (email))
            admin = User.objects.create_superuser(email=email,password=password,plan="ROOT")
            admin.is_active = True
            admin.is_admin = True
            admin.save()



        else:
            print('Admin accounts can only be initialized if no Accounts exist')