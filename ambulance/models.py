from django.db import models
from users.models import CustomUser


# Create your models here.

class Ambulance(models.Model):
    driver = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    number = models.PositiveBigIntegerField(verbose_name="ambulance number plate", unique=True, blank=False, null=False)
    status = models.CharField(max_length=50, 
        choices=(
                ("Emergency", "Emergency"),     # Life-threatening, immediate response
                ("Urgent", "Urgent"),           # Serious but not immediately life-threatening
                ("Non-Urgent", "Non-Urgent"),   # Stable condition, needs transport
                ("Routine", "Routine"),         # Scheduled or planned (e.g. hospital transfers)
                ("Low", "Low"),                 # Minor issues or consultations
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

