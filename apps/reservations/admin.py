from .models import TicketReservation, SeatAvailability, Passenger

from django.db import connection
from django.http import HttpResponse
from django.urls import path
from django.contrib import admin


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


class OLAPAdmin(admin.AdminSite):
    site_header = 'OLAP Admin Panel'

    def get_urls(self):
        urls = super().get_urls()
        olap_urls = [
            path('cumulative-bookings/', self.admin_view(self.cumulative_bookings_view), name='cumulative_bookings'),
            path('train-count/', self.admin_view(self.train_count_view), name='train_count'),
            path('revenue-share/', self.admin_view(self.revenue_share_view), name='revenue_share'),

        ]
        return olap_urls + urls

    def cumulative_bookings_view(self, request):
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT from_date, SUM(fare) AS Daily_Revenue,
                       SUM(SUM(fare)) OVER (ORDER BY from_date) AS Cumulative_Revenue
                FROM ticket_reservation
                GROUP BY from_date
                ORDER BY from_date;
            """)
            result = cursor.fetchall()

        # Format the result as HTML with styling
        html_output = '<table style="border-collapse: collapse; width: 100%; border: 1px solid #ddd;">'
        html_output += '<tr style="background-color: #f2f2f2;">'
        html_output += '<th style="padding: 8px; text-align: left; border: 1px solid #ddd;">From Date</th>'
        html_output += '<th style="padding: 8px; text-align: left; border: 1px solid #ddd;">Daily Revenue</th>'
        html_output += '<th style="padding: 8px; text-align: left; border: 1px solid #ddd;">Cumulative Revenue</th>'
        html_output += '</tr>'

        for row in result:
            html_output += '<tr>'
            for value in row:
                html_output += f'<td style="padding: 8px; border: 1px solid #ddd;">{value}</td>'
            html_output += '</tr>'

        html_output += '</table>'
        return HttpResponse(html_output)

    def train_count_view(self, request):
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT s.station_name, COUNT(r.train_id) AS TrainCount
                FROM station s
                JOIN route r ON s.station_id = r.station_id
                GROUP BY s.station_name
                ORDER BY TrainCount DESC
            """)
            result = cursor.fetchall()

        # Format the result as HTML with styling
        html_output = '<table style="border-collapse: collapse; width: 100%; border: 1px solid #ddd;">'
        html_output += '<tr style="background-color: #f2f2f2;">'
        html_output += '<th style="padding: 8px; text-align: left; border: 1px solid #ddd;">Station Name</th>'
        html_output += '<th style="padding: 8px; text-align: left; border: 1px solid #ddd;">Train Count</th>'
        html_output += '</tr>'

        for row in result:
            html_output += '<tr>'
            for value in row:
                html_output += f'<td style="padding: 8px; border: 1px solid #ddd;">{value}</td>'
            html_output += '</tr>'

        html_output += '</table>'
        return HttpResponse(html_output)

    def revenue_share_view(self, request):
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT from_date, class_id_id, SUM(fare) AS Daily_Revenue,
                       ROUND(SUM(SUM(fare)) OVER (PARTITION BY from_date) / SUM(fare), 2) AS Revenue_Share
                FROM ticket_reservation
                GROUP BY from_date, class_id_id;
            """)
            result = cursor.fetchall()

        # Format the result as HTML with styling
        html_output = '<table style="border-collapse: collapse; width: 100%; border: 1px solid #ddd;">'
        html_output += '<tr style="background-color: #f2f2f2;">'
        html_output += '<th style="padding: 8px; text-align: left; border: 1px solid #ddd;">From Date</th>'
        html_output += '<th style="padding: 8px; text-align: left; border: 1px solid #ddd;">Class ID</th>'
        html_output += '<th style="padding: 8px; text-align: left; border: 1px solid #ddd;">Daily Revenue</th>'
        html_output += '<th style="padding: 8px; text-align: left; border: 1px solid #ddd;">Revenue Share</th>'
        html_output += '</tr>'

        for row in result:
            html_output += '<tr>'
            for value in row:
                html_output += f'<td style="padding: 8px; border: 1px solid #ddd;">{value}</td>'
            html_output += '</tr>'

        html_output += '</table>'
        return HttpResponse(html_output)


# Register the OLAPAdmin site
olap_admin_site = OLAPAdmin(name='olap_admin')
olap_admin_site.register(Passenger)  # Register your models as needed
