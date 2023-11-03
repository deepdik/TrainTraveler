import csv
import os
from datetime import datetime
from django.core.management.base import BaseCommand

from apps.reservations.models import SeatAvailability
from apps.train_class.models import TrainClass
from apps.trains.models import Train


class Command(BaseCommand):
    help = 'Load data from seat availability CSV file into the SeatAvailability model'

    def handle(self, *args, **options):
        # Specify the path to your seat availability CSV file
        command_dir = os.path.dirname(__file__)

        # Specify the relative path to the CSV file in the same directory
        csv_file = os.path.join(command_dir, 'SeatAvailabaility.csv')

        try:
            with open(csv_file, 'r') as file:
                csv_reader = csv.DictReader(file)

                for row in csv_reader:
                    train_id = int(row['TrainId'])
                    class_id = int(row['ClassId'])

                    # Convert date strings to the "YYYY-MM-DD" format
                    start_date = datetime.strptime(row['StartDate'], '%m/%d/%Y').strftime('%Y-%m-%d')
                    total_seats = int(row['TotalSeats'])
                    booked_seats = int(row['BookedSeats'])

                    # Fetch the train and class records
                    train = Train.objects.get(train_id=train_id)
                    train_class = TrainClass.objects.get(class_id=class_id)

                    # Create the SeatAvailability record
                    seat_availability = SeatAvailability(
                        train=train,
                        class_id=train_class,
                        start_date=start_date,
                        total_seats=total_seats,
                        booked_seats=booked_seats,
                    )
                    seat_availability.save()

                    self.stdout.write(self.style.SUCCESS(
                        f'Successfully loaded seat availability for Train ID {train_id}, Class ID {class_id}, Date {start_date}'))

        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f'CSV file not found at {csv_file}'))
