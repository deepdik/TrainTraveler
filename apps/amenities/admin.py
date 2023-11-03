from django.contrib import admin
from .models import Amenities, AmenitiesClass


class AmenitiesAdmin(admin.ModelAdmin):
    list_display = ('amenity_id', 'name', 'description', 'image', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name', 'description')


admin.site.register(Amenities, AmenitiesAdmin)


class AmenitiesClassAdmin(admin.ModelAdmin):
    list_display = ('class_id', 'amenity')
    list_filter = ('class_id',)
    search_fields = ('class_id__class_name', 'amenity__name')


admin.site.register(AmenitiesClass, AmenitiesClassAdmin)
