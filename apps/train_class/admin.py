from django.contrib import admin
from .models import TrainClass


class TrainClassAdmin(admin.ModelAdmin):
    list_display = ('class_id', 'class_name', 'capacity', 'fare')
    list_filter = ('class_name',)
    search_fields = ('class_name',)


admin.site.register(TrainClass, TrainClassAdmin)
