# forms.py
from django import forms
from .models import TicketReservation, Passenger


class TicketReservationForm(forms.ModelForm):
    class Meta:
        model = TicketReservation
        fields = ['train', 'from_station', 'to_station', 'from_date', 'to_date', 'class_id', 'fare']


class PassengerForm(forms.ModelForm):
    class Meta:
        model = Passenger
        fields = ['first_name', 'last_name', 'dob']
