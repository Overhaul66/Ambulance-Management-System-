from django.db import models
from users.models import CustomUser

# Create your models here.
class Notification(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="notifcations_sent")
    receiver = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="notifications_recieved")
    date = models.DateTimeField(auto_now=True)
    content = models.CharField(max_length=1000)
