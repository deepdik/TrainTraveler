from django.urls import path

from apps.reservations.views import ReservationView, BookedTicketsView, ReservationSuccessView

urlpatterns = [
    path('', ReservationView.as_view(), name='reservation'),
    path('reservation/success/', ReservationSuccessView.as_view(), name='reservation_success'),
    path('history/', BookedTicketsView.as_view(), name='history'),

]