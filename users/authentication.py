from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from users.models import CustomUser

class EmailOrPhoneModelBackend(ModelBackend):
    """
    Authentication backend which allows users to authenticate using either their
    email address or phone number.
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # Check if the provided username is an email or phone number
            # and query the user accordingly
            user = CustomUser.objects.get(
                Q(email=username) | Q(phone_number=username)
            )
            
            if user.check_password(password):
                return user
        except CustomUser.DoesNotExist:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a nonexistent user
            CustomUser().set_password(password)
        
        return None