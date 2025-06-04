# users/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, OTPVerification, IndividualProfile, HealthWorkerProfile, DriverProfile
from django.contrib.auth.models import Permission

# class CustomUserAdmin(UserAdmin):
#     # Specify the fields to be displayed in the admin interface
#     model = CustomUser
#     list_display = ('email', 'phone_number', 'is_active', 'is_staff', 'is_superuser')
#     list_filter = ('is_active', 'is_staff', 'is_superuser')
#     search_fields = ('email', 'phone_number')
#     ordering = ('email',)
#     fieldsets = (
#         (None, {'fields': ('email', 'phone_number', 'password')}),
#         ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
#     )
#     add_fieldsets = (
#         (None, {
#             'classes': ('wide',),
#             'fields': ('email', 'phone_number', 'password1', 'password2', 'is_active', 'is_staff', 'is_superuser')}
#         ),
#     )
#     # Ensure that the password is hashed
#     def save_model(self, request, obj, form, change):
#         if not change:  # If creating a new user
#             obj.set_password(form.cleaned_data['password'])
#         super().save_model(request, obj, form, change)

# Register the custom user model with the admin site
admin.site.register([CustomUser,OTPVerification,HealthWorkerProfile,IndividualProfile,Permission, DriverProfile])
