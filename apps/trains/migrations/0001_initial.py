# Generated by Django 4.0 on 2023-11-03 17:10

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Train',
            fields=[
                ('train_id', models.AutoField(primary_key=True, serialize=False)),
                ('distance', models.SmallIntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('train_name', models.CharField(max_length=100)),
                ('frequency', models.SmallIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1)])),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
            ],
        ),
    ]
