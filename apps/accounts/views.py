from datetime import datetime
import random

from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User, AuthReqs, VerificationCode, \
    CODE_VERIFICATION_TIME_LIMIT


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def generate_code(phone_number: str):
    code = str(random.randint(10000, 99999))
    VerificationCode.objects.create(
        phone_number=phone_number, code=code
    )
    return code


class AuthPhoneNumberView(APIView):

    @staticmethod
    def post(request, *args, **kwargs):
        response = {
            'active_user': True if User.objects.filter(
                phone_number=request.data.get('phone_number')
            ).exists() else False
        }

        if not response['active_user']:
            code = generate_code(request.data.get('phone_number'))
            # todo: call the function responsible for sending the code
            print(f'code: {code}')
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
                status=AuthReqs.PASSWORD
            )
            return Response({'error': 'incorrect password'}, status=status.HTTP_400_BAD_REQUEST)


class RegisterCodeView(APIView):

    @staticmethod
    def post(request, *args, **kwargs):
        try:
            if not VerificationCode.objects.filter(
                    code=request.data.get('code'),
                    phone_number=request.session.get('user_id')
            ).exist:
                AuthReqs.objects.create(
                    ip_addr=get_client_ip(request),
                    phone_number=request.session.get('user_id'),
                    status=AuthReqs.VERIFICATION_CODE
                )
                return Response({'error': 'code not accepted'}, status=status.HTTP_400_BAD_REQUEST)

            if VerificationCode.objects.get(
                    code=request.data.get('code'),
                    phone_number=request.session.get('user_id')
            ).created_on < datetime.now() - CODE_VERIFICATION_TIME_LIMIT:
                AuthReqs.objects.create(
                    ip_addr=get_client_ip(request),
                    phone_number=request.session.get('user_id'),
                    status=AuthReqs.VERIFICATION_CODE
                )
                return Response({'error': 'code expired'}, status=status.HTTP_400_BAD_REQUEST)

            return Response({'message': 'code accepted'}, status=status.HTTP_200_OK)

        except:
            AuthReqs.objects.create(
                ip_addr=get_client_ip(request),
                phone_number=request.session.get('user_id'),
                status=AuthReqs.VERIFICATION_CODE
            )
            return Response({'error': 'code not accepted'}, status=status.HTTP_400_BAD_REQUEST)
