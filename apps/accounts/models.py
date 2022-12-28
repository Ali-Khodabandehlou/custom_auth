import datetime

from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models

CODE_VERIFICATION_TIME_LIMIT = datetime.timedelta(minutes=3)  # in minutes


class CustomUserManager(UserManager):
    def create_user(self, phone_number, password=None, **extra_fields):
        user = self.model(
            phone_number=phone_number, **extra_fields
        )
        user.set_password(password)
        user.is_active = True
        user.save()
        return user

    def create_superuser(self, phone_number, password=None, **extra_fields):
        user = self.create_user(phone_number, password, **extra_fields)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user


class User(AbstractUser):
    phone_number = models.CharField(max_length=16, unique=True)
    email = models.CharField(max_length=200, unique=True)
    password = models.CharField(max_length=200)
    username = None
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()


class VerificationCode(models.Model):
    phone_number = models.CharField(max_length=16)
    code = models.CharField(max_length=6)

    created_on = models.DateTimeField(auto_now_add=True)


class AuthReqs(models.Model):
    ip_addr = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=16)

    PASSWORD = 'password'
    VERIFICATION_CODE = 'verification code'
    STATUS_CHOICES = (
        (PASSWORD, 'password'),
        (VERIFICATION_CODE, 'verification code'),
    )
    status = models.CharField(max_length=50, choices=STATUS_CHOICES)

    created_on = models.DateTimeField(auto_now_add=True)
