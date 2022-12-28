from django.urls import path

from .views import AuthPhoneNumberView, LoginView

urlpatterns = [
    path('phone/', AuthPhoneNumberView.as_view(), name='auth_phone'),
    path('login/', LoginView.as_view(), name='login'),
]
