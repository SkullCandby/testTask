import csv
from django.core.management.base import BaseCommand
from testTask.models import Car, Location
import random
import string


class Command(BaseCommand):
    help = 'Populate DB with random cars and locations'

    def handle(self, *args, **options):
        for _ in range(20):
            number = str(random.randint(1000, 9999)) + random.choice(string.ascii_uppercase)
            location = Location.objects.order_by('?').first()
            carrying_capacity = random.randint(1, 1000)
            Car.objects.create(number=number, location=location, carrying_capacity=carrying_capacity)
        self.stdout.write(self.style.SUCCESS('Successfully populated database!'))

    def import_data_from_csv(self):
        with open('uszips.csv', 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                location = Location(
                    zip=row["zip"],
                    lat = row["lat"],
                    lng = row["lng"],
                    city = row["city"],
                    state = row["state_name"],
                )
                location.save()
