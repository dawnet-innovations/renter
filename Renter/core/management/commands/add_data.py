import json

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import transaction

from core import models


class Command(BaseCommand):
    help = 'Add data from JSON'

    def create_superuser(self):
        user = get_user_model()
        if not user.objects.filter(username='root').exists():
            user.objects.create_superuser(username='root', password='root')
            self.stdout.write(self.style.SUCCESS(f'Successfully created superuser: root'))
        else:
            self.stdout.write(self.style.SUCCESS(f'Superuser "root" already exists'))

    def add_entries(self, json_data):
        pass

    def handle(self, *args, **options):
        pass
