from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User


class AuthPhoneNumberView(APIView):

    @staticmethod
    def post(request, *args, **kwargs):
        response = {
            'active_user': True if User.objects.filter(
                phone_number=request.data.get('phone_number')
            ).exists() else False
        }

        request.session['phone_number'] = request.data.get('phone_number')
        return Response(response, status=status.HTTP_200_OK)


class LoginView(APIView):

    @staticmethod
    def post(request, *args, **kwargs):
        try:
            user = authenticate(
                request, username=request.session.get('phone_number'),
                password=request.data.get('password')
            )
            return Response(status=status.HTTP_200_OK)
        except:
            pass
