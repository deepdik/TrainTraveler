import csv
import os
from django.core.management.base import BaseCommand

from apps.trains.models import Train


class Command(BaseCommand):
    help = 'Load train data from a CSV file and save it to the Train model'

    def handle(self, *args, **kwargs):
        # Specify a relative path to the CSV file if it's in the same directory as this command
        command_dir = os.path.dirname(__file__)

        # Specify the relative path to the CSV file in the same directory
        csv_file = os.path.join(command_dir, 'trains.csv')

        try:
            with open(csv_file, 'r') as file:
                csv_reader = csv.DictReader(file)

                for row in csv_reader:
                    train_id = int(row['Train ID'])
                    distance = int(row['Distance'])
                    train_name = row['TrainName']
                    frequency = int(row['Frequency'])
                    start_time = row['StartTime']
                    end_time = row['EndTime']

                    # Create or update the train record
                    train, created = Train.objects.get_or_create(train_id=train_id,
                                                                 distance=distance,train_name=train_name,
                                                                 frequency=frequency, start_time=start_time,
                                                                 end_time=end_time)

                    self.stdout.write(self.style.SUCCESS(f'Successfully loaded train: {train_name}'))

        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f'CSV file not found at {csv_file}'))
