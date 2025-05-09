from django.urls import path
from .views import RequestRideView

urlpatterns = [
    path('request-ride/', RequestRideView.as_view(), name='request-ride'),
]