from django.contrib import admin
from .models import Station, Route


class StationAdmin(admin.ModelAdmin):
    list_display = ('station_name', 'station_code', 'zone', 'address')
    search_fields = ('station_name', 'station_code', 'zone')
    list_filter = ('zone',)


admin.site.register(Station, StationAdmin)


class RouteAdmin(admin.ModelAdmin):
    list_display = ('station', 'train', 'arrival_time', 'departure_time', 'sequence_no')
    list_filter = ('station', 'train')
    search_fields = ('station__station_name', 'train__train_name')


admin.site.register(Route, RouteAdmin)
