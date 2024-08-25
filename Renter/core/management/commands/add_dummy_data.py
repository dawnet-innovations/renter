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

    def add_buildings(self, json_data):
        instances = [models.Building(**data) for data in json_data]
        models.Building.objects.bulk_create(instances)
        self.stdout.write(self.style.SUCCESS('Successfully added Building entries'))

    def add_rooms(self, json_data):
        buildings = {b.id: models.Building.objects.get(id=b.id) for b in models.Building.objects.all()}
        rooms = [models.Room(name=data['name'], building=buildings[data['building']]) for data in json_data]
        models.Room.objects.bulk_create(rooms)
        self.stdout.write(self.style.SUCCESS('Successfully added Room entries'))

    def add_renters(self, json_data):
        rooms = {r.id: models.Room.objects.get(id=r.id) for r in models.Room.objects.all()}
        renters = [models.Renter(
            name=data['name'],
            phone=data['phone'],
            whatsapp=data['whatsapp'],
            agreement_start=data['agreement_start'],
            agreement_end=data['agreement_end'],
            advance=data['advance'],
            rent=data['rent'],
            room=rooms[data['room']]
        ) for data in json_data]
        models.Renter.objects.bulk_create(renters)
        self.stdout.write(self.style.SUCCESS('Successfully added Renter entries'))

    def add_rents(self, json_data):
        renters = {r.id: models.Renter.objects.get(id=r.id) for r in models.Renter.objects.all()}
        rents = [models.Rent(
            renter=renters[data['renter']],
            amount_paid=data['amount_paid'],
            balance=data['balance'],
            date=data['date']
        ) for data in json_data]
        models.Rent.objects.bulk_create(rents)
        self.stdout.write(self.style.SUCCESS('Successfully added Rent entries'))

    def handle(self, *args, **options):
        self.create_superuser()

        try:
            with transaction.atomic():
                with open("core/management/commands/data.json", "r") as json_file:
                    json_data = json.load(json_file)
                    self.add_buildings(json_data["buildings"])
                    self.add_rooms(json_data["rooms"])
                    self.add_renters(json_data["renters"])
                    self.add_rents(json_data["rents"])
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'Error occurred: {e}'))
            self.stdout.write(self.style.ERROR('Rolling back changes due to an error.'))
            raise
