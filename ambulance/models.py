from django.db import models
from users.models import CustomUser


# Create your models here.

class Ambulance(models.Model):
    driver = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    number = models.PositiveBigIntegerField(verbose_name="ambulance number plate", unique=True, blank=False, null=False)
    status = models.CharField(max_length=50, 
        choices=(
            ("Available", "available"),
            ("Unavailable", "unavailable"),
            ("Busy", "busy"),
            ("Arrived", "arrived"),
            ("On-Route", "on-route")
        )
    )
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
   

class AmbulanceRequest(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    request_date = models.DateTimeField(auto_now_add=True)
    destination = models.CharField(max_length=255)
    priority = models.CharField(max_length=10, choices=(("High", "high"), ("Medium", "medium"), ("Low", "low")))

    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

class Notification(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="notifcations_sent")
    receiver = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="notifications_recieved")
    date = models.DateTimeField(auto_now=True)
    content = models.CharField(max_length=1000)
