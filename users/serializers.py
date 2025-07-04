from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers
from .models import CustomUser, Organization
from django.contrib.auth.models import Group
from django.db import transaction

class OrganizationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Organization
        fields = ['org_name', 'address'] 

class UserSerializer(serializers.ModelSerializer):
    # Override the phone_number field to properly handle None values
    phone_number = PhoneNumberField(allow_null=True, required=False)
    organization = OrganizationSerializer(required=False, allow_null=True)
    
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
                  'age',
                  'organization',
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
    
    def create(self, validated_data):
        # if there is an error there is no db is not touched
        # prevent rain conditions
        with transaction.atomic():
            org_data = validated_data.pop('organization', None)
            role = validated_data['role']
            user = self.context['request'].user

            if org_data:
                organization, created = Organization.objects.get_or_create(
                        org_name=org_data.get('org_name'),
                        defaults={'address': org_data.get('address')}
                )
                if created and (role == "HealthAdmin" or role == "DriverAdmin"):
                    user = CustomUser.objects.create(organization=organization, **validated_data)
                elif not created and user.groups.filter(name__in=["health_admin", "admin_driver"]).exists():
                    user = CustomUser.objects.create(organization=organization, **validated_data)
                else:
                    raise serializers.ValidationError("You ain't an Admin, contact your admin")
            else:
                user = CustomUser.objects.create(**validated_data)
            
            if role == "Doctor":
                health_workers = Group.objects.get(name="healthworker")
                user.groups.add(health_workers)
            elif role == "HealthAdmin":
                health_admin = Group.objects.get(name="health_admin")
                user.groups.add(health_admin)
            elif role == "DriverAdmin":
                driver_admin = Group.objects.get(name="driver_admin")
                user.groups.add(driver_admin)
            elif role == "Driver":
                driver = Group.objects.get(name="driver")
                user.groups.add(driver)
            elif role == "Individual":
                individual = Group.objects.get(name="individual")
                user.groups.add(individual)

            
            return user


