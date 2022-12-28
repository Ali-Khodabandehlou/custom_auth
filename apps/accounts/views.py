from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User, AuthReqs


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


class AuthPhoneNumberView(APIView):

    @staticmethod
    def post(request, *args, **kwargs):
        response = {
            'active_user': True if User.objects.filter(
                phone_number=request.data.get('phone_number')
            ).exists() else False
        }

        if not response['active_user']:
            # todo: call the function responsible for code generation and
            #       sending an sms
            pass

        request.session['user_id'] = request.data.get('user_id')
        return Response(response, status=status.HTTP_200_OK)


class LoginView(APIView):

    @staticmethod
    def post(request, *args, **kwargs):
        try:
            user = authenticate(
                request, username=request.session.get('user_id'),
                password=request.data.get('password')
            )
            return Response(status=status.HTTP_200_OK)
        except:
            AuthReqs.objects.create(
                ip_addr=get_client_ip(request),
                phone_number=request.session.get('user_id'),
                status=AuthReqs.FAILED
            )
            return Response({'error': 'incorrect password'}, status=status.HTTP_400_BAD_REQUEST)


class RegisterCodeView(APIView):

    @staticmethod
    def post(request, *args, **kwargs):
        try:
            pass
        except:
            pass
