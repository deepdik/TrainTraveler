from django.db import models
from django.core.validators import MinValueValidator


class Train(models.Model):
    train_id = models.AutoField(primary_key=True)
    distance = models.SmallIntegerField(validators=[MinValueValidator(1)])
    train_name = models.CharField(max_length=100)
    frequency = models.SmallIntegerField(default=1, validators=[MinValueValidator(1)])
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return self.train_name
    class Meta:
        db_table = 'train'