from datetime import datetime

from django.db.models import Q, F, ExpressionWrapper, Value
from django.db.models.functions import Cast
from django.forms import IntegerField
from django.shortcuts import render
from django.views import View
from rest_framework import fields

from apps.amenities.models import AmenitiesClass, Amenities
from apps.reservations.models import SeatAvailability, Passenger
from apps.stations.models import Route


# views.py
from django.views import View
from django.shortcuts import render
from datetime import datetime
from django.db.models import Q

from apps.train_class.models import TrainClass
from apps.trains.models import Train


class TrainListView(View):
    template_name = 'train_list.html'

    def get(self, request, *args, **kwargs):
        from_station_id = request.GET.get('from_station_id')
        to_station_id = request.GET.get('to_station_id')
        travel_date = request.GET.get('travel_date')
        class_id = request.GET.get('class_id')
        sort_by = request.GET.get('sort_by')
        add_ons = request.GET.get('add_ons')

        try:
            travel_date = datetime.strptime(travel_date, '%Y-%m-%d').date()
        except ValueError:
            return render(request, self.template_name, {'error': 'Invalid date format'})

        if class_id:
            # Get the trains that have the specified class
            trains_with_class = SeatAvailability.objects.filter(class_id=class_id).values_list('train',
                                                                                               flat=True).distinct()
            # Get routes for the specified stations and trains with the specified class
            routes_from_station = Route.objects.filter(station_id=from_station_id, train__in=trains_with_class)
            routes_to_station = Route.objects.filter(station_id=to_station_id, train__in=trains_with_class)
        else:
            routes_from_station = Route.objects.filter(station_id=from_station_id)
            routes_to_station = Route.objects.filter(station_id=to_station_id)

        # Find trains that start from from_station and go to to_station based on sequence numbers
        trains_between_stations = set()

        for route_from in routes_from_station:
            for route_to in routes_to_station:
                if route_from.train == route_to.train and route_from.sequence_no < route_to.sequence_no:
                    # Consider it as a train between the two stations
                    train = route_from.train
                    train.to_station = route_to.station
                    train.from_station = route_from.station
                    train.departure_time = route_from.departure_time
                    train.arrival_time = route_to.arrival_time

                    departure_datetime = datetime.combine(travel_date, route_from.departure_time)
                    arrival_datetime = datetime.combine(travel_date, route_to.arrival_time)
                    # Calculate the duration
                    duration = arrival_datetime - departure_datetime

                    # Access the duration in hours and minutes
                    duration_hours, duration_minutes = divmod(duration.seconds, 3600)
                    duration_minutes //= 60
                    train.duration = duration_minutes
                    train.d_from_date = departure_datetime
                    train.a_to_date = arrival_datetime
                    trains_between_stations.add(train)

        # Sort trains based on departure_time or duration_minutes
        if sort_by == 'departureTime':
            trains_between_stations = sorted(trains_between_stations, key=lambda x: x.departure_time)
        elif sort_by == 'shortestTrip':
            trains_between_stations = sorted(trains_between_stations, key=lambda x: x.duration)

        # this is not good practices
        for train in trains_between_stations:
            # Assuming travel_date is a variable holding the desired date
            seat_availabilities = SeatAvailability.objects.filter(
                train=train,
            )

            class_ids = set()
            print(seat_availabilities)

            for seat in seat_availabilities:
                class_ids.add(seat.class_id)
                num_passengers = Passenger.objects.filter(
                    ticket_id__train=train,
                    ticket_id__from_date=travel_date,
                    ticket_id__class_id=seat.class_id
                ).count()
                print(num_passengers, "num_passengers", seat.total_seats)
                seat.seat_available = seat.total_seats - num_passengers

            train.seat_availabilities = seat_availabilities

            amenities = AmenitiesClass.objects.filter(
                class_id__in=class_ids,
            )
            train.amenities = amenities

        # Add code to retrieve 'addons' and 'classes' data
        addons = Amenities.objects.filter(is_active=True)  # Replace YourAddonModel with your actual model
        classes = TrainClass.objects.all()  # Replace YourClassModel with your actual model

        context = {
            'trains': trains_between_stations,
            'addons': addons,
            'classes': classes,
            'add_ons': add_ons,
            'sort_by': sort_by,
            'class_id': class_id,
            "from_station_id": from_station_id,
            'to_station_id': to_station_id,
            'travel_date': travel_date
        }

        return render(request, self.template_name, context)



