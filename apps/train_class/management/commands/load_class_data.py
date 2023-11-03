import csv
import os

from django.core.management.base import BaseCommand

from apps.train_class.models import TrainClass


class Command(BaseCommand):
    help = 'Load class data from a CSV file and save it to the TrainClass model'

    def handle(self, *args, **options):
        command_dir = os.path.dirname(__file__)

        # Specify the relative path to the CSV file in the same directory
        csv_file = os.path.join(command_dir, 'class.csv')

        try:
            with open(csv_file, 'r') as file:
                csv_reader = csv.DictReader(file)

                for row in csv_reader:
                    print(row)
                    class_id = int(row['\ufeffClassId'])
                    class_name = row['ClassName']
                    capacity = int(row['Capacity'])
                    fare = float(row['Fare'])

                    # Create or update the class record
                    train_class, created = TrainClass.objects.get_or_create(class_id=class_id,
                                                                            class_name=class_name,
                                                                            capacity=capacity,
                                                                            fare=fare)

                    self.stdout.write(self.style.SUCCESS(f'Successfully loaded class: {class_name}'))

        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f'CSV file not found at {csv_file}'))
