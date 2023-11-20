from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, UserEmail


class CustomUserAdmin(UserAdmin):
    list_display = (
    'phone_no', 'first_name', 'last_name', 'dob', 'gender', 'type', 'is_active', 'is_staff', 'date_joined')
    list_filter = ('is_active', 'is_staff', 'type', 'gender')
    search_fields = ('phone_no', 'first_name', 'last_name')
    fieldsets = (
        (None, {'fields': ('phone_no', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'dob', 'gender', 'type')}),
        # ('Permissions', {'fields': ('is_active', 'is_staff', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone_no', 'password1', 'password2'),
        }),
    )
    ordering = ('date_joined',)


admin.site.register(User, CustomUserAdmin)

admin.site.register(UserEmail)
