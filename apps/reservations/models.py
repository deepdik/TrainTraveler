from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.train_class.models import TrainClass
from apps.trains.models import Train
from apps.users.models import User
from django.core.validators import MinValueValidator


class TicketReservation(models.Model):
    TICKET_STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Cancelled', 'Cancelled'),
    ]
    ticket_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    train = models.ForeignKey(Train, on_delete=models.CASCADE)
    from_station = models.CharField(max_length=50)
    to_station = models.CharField(max_length=50)
    from_date = models.DateField()
    to_date = models.DateField()
    class_id = models.ForeignKey(TrainClass, on_delete=models.CASCADE)
    fare = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)])
    status = models.CharField(max_length=20, choices=TICKET_STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    total_passenger = models.IntegerField(default=0)

    def __str__(self):
        return f"Ticket ID: {self.ticket_id}, Train: {self.train.train_name}, Phone: {self.user}"

    class Meta:
        unique_together = ('ticket_id', 'train', 'user', 'class_id')

    class Meta:
        db_table = 'ticket_reservation'


class Passenger(models.Model):
    ticket_id = models.ForeignKey('TicketReservation', on_delete=models.CASCADE, related_name="passengers")
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    dob = models.DateField()

    class Meta:
        db_table = 'ticket_passenger'


## trigger to update passanger number
@receiver(post_save, sender=Passenger)
def update_total_passenger(sender, instance, **kwargs):
    # Update total_passenger when a new Passenger is added or an existing one is updated/deleted
    ticket_reservation = instance.ticket_id
    ticket_reservation.total_passenger = ticket_reservation.passengers.count()
    ticket_reservation.save()


# Connect the signal
post_save.connect(update_total_passenger, sender=Passenger)


class SeatAvailability(models.Model):
    train = models.ForeignKey(Train, on_delete=models.CASCADE, related_name="train_seat_availability")
    class_id = models.ForeignKey(TrainClass, on_delete=models.CASCADE, related_name="class_seat_availability")

    total_seats = models.IntegerField(validators=[MinValueValidator(1)])

    # booked_seats = models.IntegerField()

    class Meta:
        unique_together = ('train', 'class_id',)
        indexes = [
            models.Index(fields=['train', 'class_id'])
        ]

    def __str__(self):
        return f"Train: {self.train.train_name}, Class: {self.class_id.class_name}"

    class Meta:
        db_table = 'seat_availability'


