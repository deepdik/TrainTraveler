from django.db import models

from apps.train_class.models import TrainClass
from apps.trains.models import Train
from apps.users.models import User
from django.core.validators import MinValueValidator


class TicketReservation(models.Model):
    ticket_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    train = models.ForeignKey(Train, on_delete=models.CASCADE)
    from_station = models.CharField(max_length=50)
    to_station = models.CharField(max_length=50)
    from_date = models.DateField()
    to_date = models.DateField()
    class_id = models.ForeignKey(TrainClass, on_delete=models.CASCADE)
    fare = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)])

    def __str__(self):
        return f"Ticket ID: {self.ticket_id}, Train: {self.train.train_name}, Phone: {self.phoneno}"

    class Meta:
        unique_together = ('ticket_id', 'train', 'user', 'class_id')

    class Meta:
        db_table = 'ticket_reservation'

class SeatAvailability(models.Model):
    train = models.ForeignKey(Train, on_delete=models.CASCADE)
    class_id = models.ForeignKey(TrainClass, on_delete=models.CASCADE)
    start_date = models.DateField()
    total_seats = models.IntegerField(validators=[MinValueValidator(1)])
    booked_seats = models.IntegerField()

    class Meta:
        unique_together = ('train', 'class_id', 'start_date')

    def __str__(self):
        return f"Train: {self.train.train_name}, Class: {self.class_id.class_name}, Date: {self.start_date}"

    class Meta:
        db_table = 'seat_availability'