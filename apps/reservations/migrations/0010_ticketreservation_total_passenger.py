# Generated by Django 4.0 on 2023-11-21 04:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0009_remove_seatavailability_booked_seats'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticketreservation',
            name='total_passenger',
            field=models.IntegerField(default=0),
        ),
    ]
