from django.contrib import admin
from .models import Train


class TrainAdmin(admin.ModelAdmin):
    list_display = ('train_id', 'train_name', 'distance', 'frequency', 'start_time', 'end_time')
    search_fields = ('train_id', 'train_name', 'distance', 'frequency', 'start_time', 'end_time')
    list_filter = ('frequency',)


admin.site.register(Train, TrainAdmin)
