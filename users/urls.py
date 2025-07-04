from django.urls import path
from .views import (
    UserCreateAPIView,
    LoginView,
    VerifyEmailView,
    RequestVerificationCode,
    ManageUsersView,
)


urlpatterns = [
    path("register/", UserCreateAPIView.as_view(), name="register"),
    path("organization/", ManageUsersView.as_view(), name="organization users"),
    path("login/", LoginView.as_view(), name="login"),
    path("verify-email/", VerifyEmailView.as_view(), name="verify-email"),
    path("request-otp/", RequestVerificationCode.as_view(), name="request-otp" )
]