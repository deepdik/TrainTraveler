# Generated by Django 4.0 on 2023-11-03 18:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stations', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='route',
            name='arrival_time',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='route',
            name='departure_time',
            field=models.TimeField(blank=True, null=True),
        ),
    ]
