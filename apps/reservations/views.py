from datetime import date

from django.contrib.auth.decorators import login_required
from django.db import connections
from django.db.models import Count
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View

from apps.reservations.forms import TicketReservationForm, PassengerForm
from apps.reservations.models import TicketReservation, Passenger, SeatAvailability
from apps.train_class.models import TrainClass
from apps.trains.models import Train


@method_decorator(login_required, name='dispatch')
class ReservationView(View):
    template_name = 'reservation.html'

    def get(self, request, *args, **kwargs):
        # Get parameters from the URL
        train_id = request.GET.get('train_id', '')
        from_station = request.GET.get('from_station', '')
        to_station = request.GET.get('to_station', '')
        from_date = request.GET.get('from_date', '')
        to_date = request.GET.get('to_date', '')
        class_id = request.GET.get('class_id', '')

        # Create a dictionary to pre-fill the form
        initial_data = {
            'train': Train.objects.get(train_id=train_id),
            'from_station': from_station,
            'to_station': to_station,
            'from_date': from_date,
            'to_date': to_date,
            'class_id': TrainClass.objects.get(class_id=class_id),
            # Add more fields if needed
        }

        return render(request, self.template_name, context=initial_data)

    def post(self, request, *args, **kwargs):
        # Extract data from the form submission
        from_station = request.POST.get('from_station', '')
        to_station = request.POST.get('to_station', '')
        from_date = request.POST.get('from_date', '')
        to_date = request.POST.get('to_date', '')
        base_fare = request.POST.get('base_fare', '')
        total_fare = request.POST.get('total_fare', '')

        train_id = request.POST.get('train')
        train_instance = Train.objects.get(pk=train_id)

        class_id = request.POST.get('class_id')
        class_instance = TrainClass.objects.get(pk=class_id)

        # Your logic to save the data to the TicketReservation model
        reservation = TicketReservation.objects.create(
            user=request.user,
            train=train_instance,
            from_station=from_station,
            to_station=to_station,
            from_date=from_date,
            to_date=to_date,
            class_id=class_instance,
            fare=total_fare,
            status=TicketReservation.TICKET_STATUS_CHOICES[0][1]
        )

        # Extract passenger data
        passenger_first_names = request.POST.getlist('passenger_first_name')
        passenger_last_names = request.POST.getlist('passenger_last_name')
        passenger_dobs = request.POST.getlist('passenger_dob')

        # Iterate through passenger data and save to the Passenger model
        for first_name, last_name, dob in zip(passenger_first_names, passenger_last_names, passenger_dobs):
            passenger = Passenger.objects.create(
                ticket_id=reservation,
                first_name=first_name,
                last_name=last_name,
                dob=dob,
            )

        # Redirect to a success page or return a success response
        return redirect('history')


class ReservationSuccessView(View):
    template_name = 'reservation_success.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


@method_decorator(login_required, name='dispatch')
class BookedTicketsView(View):
    template_name = 'history.html'

    def get(self, request, *args, **kwargs):
        user = request.user
        # Define your raw SQL query
        raw_sql_query = """
            SELECT
                ticket_id,
                from_date,
                to_date,
                class_id_id AS class_id,
                num_passengers
            FROM
                booked_tickets_view
            WHERE
                user_id = %s
            ORDER BY
                ticket_id DESC
        """

        # Use the database connection to execute the raw SQL query
        with connections['default'].cursor() as cursor:
            cursor.execute(raw_sql_query, [user.phone_no])
            result = cursor.fetchall()

        booked_tickets = TicketReservation.objects.filter(user=user).annotate(num_passengers=Count('passengers')).order_by("-ticket_id")
        return render(request, self.template_name, {'booked_tickets': booked_tickets, 'today_date': date.today() , "result": result})
