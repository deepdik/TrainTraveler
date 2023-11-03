import csv
import os

from django.core.management.base import BaseCommand

from apps.users.models import UserEmail, User


class Command(BaseCommand):
    help = 'Insert user email data from a CSV file into the UserEmail model'

    def handle(self, *args, **options):
        # Replace 'user_emails.csv' with the path to your CSV file
        command_dir = os.path.dirname(__file__)

        # Specify the relative path to the CSV file in the same directory
        csv_file = os.path.join(command_dir, 'user_email.csv')

        try:
            with open(csv_file, 'r') as file:
                reader = csv.reader(file)
                next(reader)  # Skip the header row

                for row in reader:
                    print(row)
                    if len(row) == 2:
                        phone_no, email = row
                        phone_no = "".join(phone_no.split("-"))
                        user = User.objects.get(phone_no=phone_no)  # Replace with your actual User model field
                        user_email, created = UserEmail.objects.get_or_create(user=user, email=email)

                        if created:
                            self.stdout.write(self.style.SUCCESS(f'Successfully inserted user email: {phone_no} - {email}'))
                        else:
                            self.stdout.write(self.style.SUCCESS(f'User email already exists: {phone_no} - {email}'))
                    else:
                        self.stdout.write(self.style.ERROR('Invalid data format in the CSV file'))

        except FileNotFoundError:
            self.stdout.write(self.style.ERROR('CSV file not found. Please provide the correct path.'))
