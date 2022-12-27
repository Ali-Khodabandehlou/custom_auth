from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User


class AuthPhoneNumber(APIView):

    @staticmethod
    def post(request, *args, **kwargs):
        phone_number = request.data.get('phone_number')

        if User.objects.get(phone_number=phone_number).exists():
            response = {
                'active_user': True
            }
        else:
            response = {
                'active_user': False
            }

        return Response(response, status=status.HTTP_200_OK)
