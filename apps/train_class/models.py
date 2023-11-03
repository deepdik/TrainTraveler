from django.db import models
from django.core.validators import MinValueValidator


class TrainClass(models.Model):
    class_id = models.AutoField(primary_key=True)
    class_name = models.CharField(max_length=30)
    capacity = models.SmallIntegerField(validators=[MinValueValidator(1)])
    fare = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(0.01)])

    def __str__(self):
        return self.class_name

    class Meta:
        db_table = 'train_class'
