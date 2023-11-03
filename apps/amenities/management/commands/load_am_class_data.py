import csv
import os

from django.core.management.base import BaseCommand

from apps.amenities.models import AmenitiesClass, Amenities
from apps.train_class.models import TrainClass


class Command(BaseCommand):
    help = 'Insert data into AmenitiesClass model from a CSV file'

    def handle(self, *args, **options):
        command_dir = os.path.dirname(__file__)

        # Specify the relative path to the CSV file in the same directory
        csv_file = os.path.join(command_dir, 'amenities_class.csv')
        self.insert_amenities_class_from_csv(csv_file)

    def insert_amenities_class_from_csv(self, csv_file):
        with open(csv_file, "r") as file:
            csv_data = csv.DictReader(file)
            for row in csv_data:
                class_id = TrainClass.objects.get(class_id=row["class_id"])
                amenity = Amenities.objects.get(amenity_id=row["amenity_id"])
                amenities_class = AmenitiesClass(
                    class_id=class_id,
                    amenity=amenity,
                )
                amenities_class.save()
                self.stdout.write(self.style.SUCCESS(f'Successfully inserted data into AmenitiesClass: Class ID {class_id.class_id} - Amenity ID {amenity.amenity_id}'))
