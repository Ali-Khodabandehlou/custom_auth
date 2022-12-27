from django.contrib import admin

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = [
        'phone_number',
        'email',
        'is_staff',
        'is_superuser',
        'last_login'
    ]
