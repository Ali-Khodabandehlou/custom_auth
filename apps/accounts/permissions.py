import datetime

from rest_framework.permissions import BasePermission

from .models import BlockedIP


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


class BlockedIPPermission(BasePermission):
    message = 'action is blocked for 1 hour'

    def has_permission(self, request, view):
        if BlockedIP.objects.filter(
            ip_addr=get_client_ip(request),
            created_on__lt=datetime.datetime.now() - datetime.timedelta(hours=1)
        ).exists():
            return False
        return True
