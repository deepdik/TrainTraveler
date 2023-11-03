from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import TicketReservation, SeatAvailability


class TicketReservationAdmin(admin.ModelAdmin):
    list_display = (
    'ticket_id', 'user', 'train', 'from_station', 'to_station', 'from_date', 'to_date', 'class_id', 'fare')
    list_filter = ('from_date', 'to_date', 'class_id')
    search_fields = ('ticket_id', 'user__phone_no', 'train__train_name', 'from_station', 'to_station')


admin.site.register(TicketReservation, TicketReservationAdmin)


class SeatAvailabilityAdmin(admin.ModelAdmin):
    list_display = ('train', 'class_id', 'start_date', 'total_seats', 'booked_seats')
    list_filter = ('train', 'class_id', 'start_date')
    search_fields = ('train__train_name', 'class_id__class_name', 'start_date')


admin.site.register(SeatAvailability, SeatAvailabilityAdmin)
