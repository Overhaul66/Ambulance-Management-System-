from datetime import datetime, timedelta
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError

from .managers import CustomUserManager

class CustomUser(AbstractUser):
    username = None
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    age = models.PositiveBigIntegerField(null=True, blank=True)
    email = models.EmailField(_("email address"), unique=True, null=True, blank=True)
    phone_number = PhoneNumberField(null=True, blank=True, unique=True, verbose_name="phone number")
    email_verified = models.BooleanField(default=False)
    phone_verified = models.BooleanField(default=False)
    role = models.CharField(max_length=10, choices=[
        ("Individual", "individual"),
        ("Driver", "driver"),
        ("Admin", "admin"),
        ("Nurse", "nurse"),
        ("Doctor", "doctor"),
        ("Org_Admin", "org_admin")
    ])


    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email or (self.phone_number.as_e164 if self.phone_number else f"User-{self.id}")
    
    
    def clean(self):
        super().clean()
        if not self.email and not self.phone_number:
            raise ValidationError(_("Either email or phone number must be provided"))
        
    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(email__isnull=False) | models.Q(phone_number__isnull=False),
                name="user_has_email_or_phone"
            )
        ]

import pyotp
        
class OTPVerification(models.Model):
    
    PURPOSE_CHOICES = (
        ('EMAIL_VERIFICATION', 'Email Verification'),
        ('SMS_VERIFICATION', 'SMS verification'),
        ('PASSWORD_RESET', 'Password Reset'),
        ('TWO_FACTOR', 'Two-Factor Authentication'),
        # Add other purposes as needed
    )

    user = models.ForeignKey(CustomUser, related_name="OTPVerifications", on_delete=models.CASCADE)
    secret_key = models.CharField(max_length=32)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_verified = models.BooleanField(default=False)
    method = models.CharField(max_length=10, choices=[('email', 'Email'), ('sms', 'SMS')])
    purpose = models.CharField(max_length=20, choices=PURPOSE_CHOICES, default="EMAIL_VERIFICATION")

    def __str__(self):
        return f"{self.user.email if self.user.email else self.user.phone_number} - {self.method}"
    
    def save(self, *args, **kwargs):
        # set the expiry date on save
        if not self.expires_at:
            self.expires_at = timezone.now() + timedelta(minutes=10)

        super().save(*args, **kwargs)

    # generate otp to send to user
    def generate_otp(self):
        totp = pyotp.TOTP(self.secret_key, digits=6, interval=600)
        return totp.now()
    
    
    @classmethod
    def verify_otp(cls, token):
        valid_otps = cls.objects.filter(expires_at__gt=timezone.now())
        
        for otp in valid_otps:
            totp = pyotp.TOTP(otp.secret_key, digits=6, interval=600)
            is_valid = totp.verify(token)
            if is_valid:
                otp.is_verified = is_valid
                otp.save()
                return otp
        
        return None
      
class HealthWorkerProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    # organization

class IndividualProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

class DriverProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    
class Organization(models.Model):
    org_name = models.CharField(max_length=255, null=False, blank=False)
    address = models.CharField(max_length=255, null=False, blank=False)

