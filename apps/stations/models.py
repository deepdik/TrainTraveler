from django.db import models


class Station(models.Model):
    station_id = models.AutoField(primary_key=True)
    station_name = models.CharField(max_length=50, db_index=True)
    station_code = models.CharField(max_length=10, unique=True)
    address = models.TextField()
    zone = models.CharField(max_length=20)

    def __str__(self):
        return self.station_name

    class Meta:
        db_table = 'station'
        indexes = [
            models.Index(fields=['station_name']),
        ]


class Route(models.Model):
    station = models.ForeignKey('stations.Station', on_delete=models.CASCADE, related_name="routes_station")
    train = models.ForeignKey('trains.Train', on_delete=models.CASCADE, related_name="routes_train")
    arrival_time = models.TimeField(blank=True, null=True)
    departure_time = models.TimeField(blank=True, null=True)
    sequence_no = models.IntegerField()

    class Meta:
        unique_together = ('station', 'train')

    def __str__(self):
        return f"{self.station.station_name} on Train {self.train.train_name}"

    class Meta:
        db_table = 'route'