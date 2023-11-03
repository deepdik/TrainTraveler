import csv
import os

from django.core.management.base import BaseCommand

from apps.amenities.models import Amenities


class Command(BaseCommand):
    help = 'Insert amenities data from a CSV file'

    def handle(self, *args, **options):
        # Specify the path to your routes CSV file
        command_dir = os.path.dirname(__file__)

        # Specify the relative path to the CSV file in the same directory
        csv_file = os.path.join(command_dir, 'amenities.csv')
        self.insert_amenities_from_csv(csv_file)

    def insert_amenities_from_csv(self, csv_file):
        with open(csv_file, "r") as file:
            csv_data = csv.DictReader(file)
            for row in csv_data:
                print(row)
                amenity = Amenities(
                    amenity_id=row["AmenityId"],
                    name=row["AmenityName"],
                    description=row["AmenityDescription"],
                    image=row["image"],
                    is_active=row["isactive"] == "TRUE",
                )
                amenity.save()
                self.stdout.write(self.style.SUCCESS(f'Successfully inserted amenity: {row["AmenityName"]}'))
