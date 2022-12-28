import datetime

from django.utils import timezone
from rest_framework.exceptions import APIException
from rest_framework.permissions import BasePermission

from .models import BlockedIP, AllowedSignUpIP


def get_client_ip(request):
    """
        returns client's IP
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


class BlockedIPException(APIException):
    status_code = 403
    default_detail = 'action is blocked for 1 hour'
    default_code = 'service_unavailable'


class BlockedIPPermission(BasePermission):
    """
        permission for blocked ip/users
    """
    message = 'action is blocked for 1 hour'

    def has_permission(self, request, view):
        if BlockedIP.objects.filter(
            ip_addr=get_client_ip(request),
            created_on__lt=timezone.now() - datetime.timedelta(hours=1)
        ).exists():
            raise BlockedIPException()
        return True


class SignUpException(APIException):
    status_code = 403
    default_detail = 'new verification code required'
    default_code = 'service_unavailable'


class AllowedSignUpPermission(BasePermission):
    """
        permission for signup
        raises an exception when code verification passed 1 hour
    """
    def has_permission(self, request, view):
        if AllowedSignUpIP.objects.filter(
            ip_addr=get_client_ip(request),
            phone_number=request.session.get('user_id'),
            created_on__gte=timezone.now() - datetime.timedelta(hours=1)
        ).exists():
            return True
        raise SignUpException()
