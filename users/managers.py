from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, email=None, phone_number=None, password =None, **extra_fields):
        """
        Create and save a user with the given email and password.
        """
        if not email and not phone_number:
            raise ValueError(_("Either email or phone must be set"))
       
        if email:
            email = self.normalize_email(email)

        user = self.model(email=email, phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save()
       
        return user

    def create_superuser(self, email=None,phone_number=None, password=None, **extra_fields):
        """
         Create and save a SuperUser with the given email/phone and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        
        return self.create_user(email,phone_number, password, **extra_fields)