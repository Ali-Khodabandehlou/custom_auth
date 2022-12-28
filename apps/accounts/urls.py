from django.urls import path

from .views import AuthPhoneNumberView, LoginView, RegisterCodeView, GetUserInfoRegisterView

urlpatterns = [
    path('phone/', AuthPhoneNumberView.as_view(), name='auth_phone'),
    path('login/', LoginView.as_view(), name='login'),
    path('code/', RegisterCodeView.as_view(), name='verify_code'),
    path('register/', GetUserInfoRegisterView.as_view(), name='register'),
]
