from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers
from .models import CustomUser, HealthWorkerProfile, IndividualProfile

class UserSerializer(serializers.ModelSerializer):
    # Override the phone_number field to properly handle None values
    phone_number = PhoneNumberField(allow_null=True, required=False)
    
    class Meta:
        model = CustomUser
        fields = (
                  'id',
                  'email', 
                  'phone_number', 
                  'email_verified', 
                  'phone_verified',
                  'role',
                  'first_name',
                  'last_name',
                  'age'
                )
    
    def validate_phone_number(self, value):
        # Handle None or empty string values
        if value is None or value == "":
            return None
        return value
    
    def validate_email(self, value):
        if value is None or value == "":
            return None
        return value
    

    def validate(self, data):
        """
        Check that at least one of email or phone_number is provided.
        """
        email = data.get('email')
        phone_number = data.get('phone_number')
        
        if email is None and phone_number is None:
            raise serializers.ValidationError(
                {"error": "You must provide either a valid email address or phone number."}
            )
        
        elif email and phone_number:
            raise serializers.ValidationError(
                {"error": "Please provide only one authentication method - either email OR phone number, not both."}
      
            )
        
        return data
    
class HealthWorkerProfileSerializer(serializers.ModelSerializer):
    
    user = UserSerializer()

    class Meta():
        model = HealthWorkerProfile
        fields = ['user']

class IndividualProfileSerializer(serializers.ModelSerializer):
    pass