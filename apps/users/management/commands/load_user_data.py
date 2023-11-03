import csv
import os

from django.core.management.base import BaseCommand

from apps.users.models import User


class Command(BaseCommand):
    help = 'Load user data from a hardcoded CSV file path and save it to the User model'

    def handle(self, *args, **kwargs):
        # Hardcode the path to your CSV file here
        command_dir = os.path.dirname(__file__)

        # Specify the relative path to the CSV file in the same directory
        csv_file = os.path.join(command_dir, 'users.csv')

        try:
            with open(csv_file, 'r') as file:
                csv_reader = csv.DictReader(file)

                for row in csv_reader:
                    phone_no = "".join(row["\ufeffPhoneNo"].split("-"))
                    first_name = row['Name_FirstName']
                    last_name = row['Name_LastName']
                    dob = row['DOB']
                    gender = row['Gender']
                    password = row['Password']
                    user_type = row['UserType']

                    # Process DOB (assuming MM/DD/YY format)
                    dob_parts = dob.split('/')
                    dob = f'19{dob_parts[2]}-{dob_parts[0]}-{dob_parts[1]}'  # Convert to YYYY-MM-DD format

                    print("-----", phone_no)
                    # Create or update the user
                    user, created = User.objects.get_or_create(phone_no=phone_no)
                    user.first_name = first_name
                    user.last_name = last_name
                    user.dob = dob
                    user.set_password(password)
                    user.gender = gender
                    user.user_type = user_type
                    user.save()

                    self.stdout.write(self.style.SUCCESS(f'Successfully loaded user: {phone_no}'))

        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f'CSV file not found at {csv_file}'))
