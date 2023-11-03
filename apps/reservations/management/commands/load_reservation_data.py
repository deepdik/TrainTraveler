import csv
import os
from datetime import datetime

from django.core.management.base import BaseCommand

from apps.reservations.models import TicketReservation
from apps.train_class.models import TrainClass
from apps.trains.models import Train
from apps.users.models import User


class Command(BaseCommand):
    help = 'Load data from ticket reservation CSV file into the TicketReservation model'

    def handle(self, *args, **options):
        # Specify the path to your ticket reservation CSV file
        command_dir = os.path.dirname(__file__)

        # Specify the relative path to the CSV file in the same directory
        csv_file = os.path.join(command_dir, 'TicketReservation.csv')

        try:
            with open(csv_file, 'r') as file:
                csv_reader = csv.DictReader(file)

                for row in csv_reader:
                    print(row)
                    ticket_id = int(row['TicketId '])
                    phone_no = "".join(row['PhoneNo'].split("-"))
                    train_id = int(row['TrainId'])
                    from_station = row['FromStation']
                    to_station = row['ToStation']
                    class_id = int(row['ClassId'])
                    fare = float(row['Fare'])
                    # Convert date strings to the "YYYY-MM-DD" format
                    from_date = datetime.strptime(row['FromDate'], '%m/%d/%Y').strftime('%Y-%m-%d')
                    to_date = datetime.strptime(row['ToDate'], '%m/%d/%Y').strftime('%Y-%m-%d')


                    # Fetch the user, train, and class records
                    user = User.objects.get(phone_no=phone_no)
                    train = Train.objects.get(train_id=train_id)
                    train_class = TrainClass.objects.get(class_id=class_id)

                    # Create the TicketReservation record
                    ticket = TicketReservation(
                        ticket_id=ticket_id,
                        user=user,
                        train=train,
                        from_station=from_station,
                        to_station=to_station,
                        from_date=from_date,
                        to_date=to_date,
                        class_id=train_class,
                        fare=fare,
                    )
                    ticket.save()

                    self.stdout.write(self.style.SUCCESS(f'Successfully loaded ticket reservation: Ticket ID {ticket.ticket_id}'))

        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f'CSV file not found at {csv_file}'))
