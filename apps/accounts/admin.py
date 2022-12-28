from django.contrib import admin

from .models import User, VerificationCode, AuthReqs, AllowedSignUpIP


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = [
        'phone_number',
        'email',
        'is_staff',
        'is_superuser',
        'last_login'
    ]


@admin.register(VerificationCode)
class VerificationCodeAdmin(admin.ModelAdmin):
    list_display = [
        'phone_number',
        'code',
        'created_on'
    ]


@admin.register(AuthReqs)
class AuthReqsAdmin(admin.ModelAdmin):
    list_display = [
        'ip_addr',
        'phone_number',
        'status',
        'created_on'
    ]


@admin.register(AllowedSignUpIP)
class AllowedSignUpIPAdmin(admin.ModelAdmin):
    list_display = [
        'phone_number',
        'ip_addr',
        'created_on'
    ]
