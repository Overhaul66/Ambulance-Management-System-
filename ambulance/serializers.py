from rest_framework import serializers 
from .models import Ambulance, AmbulanceRequest

class AmbulanceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ambulance
        fields = ['driver', 'status', 'number', 'lonngitude', 'latitude']

class AmbulanceRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = AmbulanceRequest
        fields = ['priority' , 'longitude', 'latitude', 'destination']
        read_only_fields = ['user', ]  # Assuming status is set automatically