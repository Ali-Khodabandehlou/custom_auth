import datetime
import random

from django.contrib.auth import authenticate
from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User, AuthReqs, VerificationCode, \
    CODE_VERIFICATION_TIME_LIMIT, BlockedIP, AllowedSignUpIP
from .permissions import get_client_ip, BlockedIPPermission, AllowedSignUpPermission


def generate_code(phone_number: str):
    """
        generates a random verification code
    """
    code = str(random.randint(100000, 999999))
    VerificationCode.objects.create(
        phone_number=phone_number, code=code
    )
    return code


def handle_bad_requests(request, req_status):
    AuthReqs.objects.create(
        ip_addr=get_client_ip(request),
        phone_number=request.session.get('user_id'),
        status=req_status
    )

    if AuthReqs.objects.filter(
            ip_addr=get_client_ip(request),
            created_on__lt=timezone.now() - datetime.timedelta(hours=1),
            status=req_status
    ).count() >= 3:
        # blocks if bad requests were more than 3
        BlockedIP.objects.create(ip_addr=get_client_ip(request))


class AuthPhoneNumberView(APIView):
    """
        checks if the requested phone number has already signed up or not
        allowed methods: POST
        request data:
            phone_number: string - format: +98********** ('+98' followed by 10 digits)
    """

    @staticmethod
    def post(request, *args, **kwargs):
        # checks for active users
        response = {
            'active_user': True if User.objects.filter(
                phone_number=request.data.get('phone_number')
            ).exists() else False
        }

        if not response['active_user']:
            # generate code if no active user found
            code = generate_code(request.data.get('phone_number'))
            # todo: call the function responsible for sending the code
            print(f'code: {code}')
            pass

        request.session['user_id'] = request.data.get('phone_number')
        return Response(response, status=status.HTTP_200_OK)


class LoginView(APIView):
    """
        logs in using given phone number and password
        permissions: BlockedIPPermission
        allowed methods: POST
        request data:
            password: string
    """
    permission_classes = (BlockedIPPermission, )

    @staticmethod
    def post(request, *args, **kwargs):
        try:
            user = authenticate(
                request, username=request.session.get('user_id'),
                password=request.data.get('password')
            )
            return Response({'message': 'user logged in successfully'}, status=status.HTTP_200_OK)

        except:
            # handles bad requests
            handle_bad_requests(request, AuthReqs.PASSWORD)

            return Response({'error': 'incorrect password'}, status=status.HTTP_400_BAD_REQUEST)


class RegisterCodeView(APIView):
    """
        checks the verification code sent to the user
        permissions: BlockedIPPermission
        allowed methods: POST
        request data:
            code: string - format: ****** (6 digits)
    """
    permission_classes = (BlockedIPPermission, )

    @staticmethod
    def post(request, *args, **kwargs):
        try:
            if not VerificationCode.objects.filter(
                    code=request.data.get('code'),
                    phone_number=request.session.get('user_id')
            ).exists():
                # checks if code exists
                # handles bad requests
                handle_bad_requests(request, AuthReqs.VERIFICATION_CODE)

                return Response({'error': 'code not accepted'}, status=status.HTTP_400_BAD_REQUEST)

            if VerificationCode.objects.get(
                    code=request.data.get('code'),
                    phone_number=request.session.get('user_id')
            ).created_on < timezone.now() - CODE_VERIFICATION_TIME_LIMIT:
                # checks for code expiry
                # handles bad requests
                handle_bad_requests(request, AuthReqs.VERIFICATION_CODE)

                # deletes the expired code
                VerificationCode.objects.get(
                    code=request.data.get('code'),
                    phone_number=request.session.get('user_id')
                ).delete()

                return Response({'error': 'code expired'}, status=status.HTTP_400_BAD_REQUEST)

            AllowedSignUpIP.objects.create(
                phone_number=request.session.get('user_id'),
                ip_addr=get_client_ip(request)
            )
            return Response({'message': 'code accepted'}, status=status.HTTP_200_OK)

        except:
            # handles bad requests
            handle_bad_requests(request, AuthReqs.VERIFICATION_CODE)

            return Response({'error': 'code not accepted'}, status=status.HTTP_400_BAD_REQUEST)


class GetUserInfoRegisterView(APIView):
    """
        gets other user info and registers new user
        permissions: AllowedSignUpPermission
        allowed methods: POST
        request data:
            first_name: string
            last_name: string
            email: string
            password: string
            password2: string
    """
    permission_classes = (AllowedSignUpPermission, )

    @staticmethod
    def post(request, *args, **kwargs):
        try:
            if request.data.get('password') == request.data.get('password2'):
                user = User.objects.create(
                    phone_number=request.session.get('user_id'),
                    first_name=request.data.get('first_name'),
                    last_name=request.data.get('last_name')
                )
                if request.data.get('email') is not None:
                    user.email = request.data.get('email')
                user.set_password(request.data.get('password'))
                user.save()

                return Response({'user created successfuly'}, status=status.HTTP_201_CREATED)
            return Response({'error': 'passwords didn\'t match'}, status=status.HTTP_400_BAD_REQUEST)

        except:
            return Response({'error': 'something went wrong'}, status=status.HTTP_400_BAD_REQUEST)
