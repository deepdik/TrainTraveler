from django.db import models

from apps.train_class.models import TrainClass


class Amenities(models.Model):
    amenity_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    description = models.TextField()
    image = models.CharField(max_length=500, blank=True, null=True)
    is_active = models.BooleanField()

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'amenities'


class AmenitiesClass(models.Model):
    class_id = models.ForeignKey(TrainClass, on_delete=models.CASCADE)
    amenity = models.ForeignKey(Amenities, on_delete=models.CASCADE)

    def __str__(self):
        return f"Class: {self.class_id.class_name} - Amenity: {self.amenity.name}"

    class Meta:
        db_table = 'amenities_class'