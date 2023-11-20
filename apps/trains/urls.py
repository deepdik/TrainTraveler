from django.urls import path

from apps.trains.views import TrainListView

urlpatterns = [
    # path('list/', TrainListView.as_view(), name='train-list'),
    path('list/', TrainListView.as_view(), name='search_trains'),

]