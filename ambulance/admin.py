from django.contrib import admin
from . import models

# Register your models here.

admin.site.register(
    [
        models.Ambulance, 
        models.AmbulanceRequest,
        models.Notification, 
    ])
