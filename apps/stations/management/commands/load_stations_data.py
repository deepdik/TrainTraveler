import csv
import os

from django.core.management.base import BaseCommand

from apps.stations.models import Station


class Command(BaseCommand):
    help = 'Load station data from a CSV file and save it to the Station model'

    def handle(self, *args, **options):
        command_dir = os.path.dirname(__file__)

        # Specify the relative path to the CSV file in the same directory
        csv_file = os.path.join(command_dir, 'station.csv')

        try:
            with open(csv_file, 'r') as file:
                csv_reader = csv.DictReader(file)

                for row in csv_reader:
                    print(row)
                    station_id = int(row['station_id'])
                    station_name = row['station_name']
                    station_code = row['station_code']
                    address = row['address']
                    zone = row['zone\t\t\t\t'].strip()

                    # Create or update the station record
                    station, created = Station.objects.get_or_create(
                        station_id=station_id,
                        station_name=station_name,
                        station_code=station_code,
                        address=address,
                        zone=zone
                    )
                    station.station_name = station_name
                    station.station_code = station_code
                    station.address = address
                    station.zone = zone
                    station.save()

                    self.stdout.write(self.style.SUCCESS(f'Successfully loaded station: {station_name}'))

        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f'CSV file not found at {csv_file}'))
