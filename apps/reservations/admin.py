from django.contrib import admin

# Register your models here.
from django.contrib import admin

from .models import TicketReservation, SeatAvailability, Passenger


class SeatAvailabilityAdmin(admin.ModelAdmin):
    list_display = ('train', 'class_id', 'total_seats',)
    list_filter = ('train', 'class_id',)
    search_fields = ('train__train_name', 'class_id__class_name')


admin.site.register(SeatAvailability, SeatAvailabilityAdmin)


class PassengerInline(admin.TabularInline):
    model = Passenger
    extra = 0  # Set to 0 to show existing passengers, not create new ones


class TicketReservationAdmin(admin.ModelAdmin):
    list_display = ('ticket_id', 'train', 'from_station', 'to_station', 'from_date', 'to_date', 'class_id', 'fare',
                    )
    list_filter = ('from_date', 'to_date', 'class_id')
    search_fields = ('ticket_id', 'user__phone_no', 'train__train_name', 'from_station', 'to_station')
    def num_passengers(self, obj):
        return obj.passengers.count()  # Assuming you've set up a related name 'passengers' in TicketReservation model

    num_passengers.short_description = 'Number of Passengers'

    inlines = [PassengerInline]


admin.site.register(TicketReservation, TicketReservationAdmin)









