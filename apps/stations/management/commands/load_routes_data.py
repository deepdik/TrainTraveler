import csv
import os

from django.core.management.base import BaseCommand

from apps.stations.models import Station, Route
from apps.trains.models import Train


class Command(BaseCommand):
    help = 'Load data from routes CSV file into the Route model'

    def handle(self, *args, **options):
        # Specify the path to your routes CSV file
        command_dir = os.path.dirname(__file__)

        # Specify the relative path to the CSV file in the same directory
        csv_file = os.path.join(command_dir, 'Routes.csv')

        try:
            with open(csv_file, 'r') as file:
                csv_reader = csv.DictReader(file)

                for row in csv_reader:
                    print(row)
                    station_id = int(row['station_id'])
                    train_id = int(row['train_id'])
                    arrival_time = row['arrival_time']
                    if not arrival_time:
                        arrival_time = None
                    departure_time = row['departure_time']
                    if not departure_time:
                        departure_time = None
                    sequence_no = int(row['sequence_no'])

                    # Fetch the station and train records
                    station = Station.objects.get(station_id=station_id)
                    train = Train.objects.get(train_id=train_id)

                    print(departure_time, arrival_time)
                    # Create or update the Route record
                    route, created = Route.objects.get_or_create(
                        station=station, train=train, arrival_time=arrival_time,
                        departure_time=departure_time, sequence_no=sequence_no)
                    route.arrival_time = arrival_time
                    route.departure_time = departure_time
                    route.sequence_no = sequence_no
                    route.save()

                    self.stdout.write(self.style.SUCCESS(f'Successfully loaded route: {station.station_name} on Train {train.train_name}'))

        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f'CSV file not found at {csv_file}'))
