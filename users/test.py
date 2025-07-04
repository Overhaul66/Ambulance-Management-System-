from django.contrib.auth import get_user_model
from django.test import TestCase


# class UsersManagersTests(TestCase):

#     def test_create_user_with_email(self):
#         User = get_user_model()
#         user = User.objects.create_user(email="normal@user.com", password="foo")
#         self.assertEqual(user.email, "normal@user.com")
#         self.assertTrue(user.is_active)
#         self.assertFalse(user.is_staff)
#         self.assertFalse(user.is_superuser)
#         try:
#             # username is None for the AbstractUser option
#             # username does not exist for the AbstractBaseUser option
#             self.assertIsNone(user.username)
#         except AttributeError:
#             pass
#         with self.assertRaises(ValueError):
#             User.objects.create_user()
#         with self.assertRaises(ValueError):
#             User.objects.create_user(email="")
#         with self.assertRaises(ValueError):
#             User.objects.create_user(email="", password="foo")
    
#     def test_create_user_with_number(self):
#         User = get_user_model()
#         user = User.objects.create_user(phone_number="+233 50 457 2087", password="foo")
#         self.assertEqual(user.phone_number, "+233 50 457 2087")
#         self.assertTrue(user.is_active)
#         self.assertFalse(user.is_staff)
#         self.assertFalse(user.is_superuser)
#         try:
#             # username is None for the AbstractUser option
#             # username does not exist for the AbstractBaseUser option
#             self.assertIsNone(user.username)
#         except AttributeError:
#             pass
        
#         with self.assertRaises(ValueError):
#             User.objects.create_user()
#         with self.assertRaises(ValueError):
#             User.objects.create_user(phone_number="")
#         with self.assertRaises(ValueError):
#             User.objects.create_user(phone_number="", password="foo")

#     def test_create_superuser_with_email(self):
#         User = get_user_model()
#         admin_user = User.objects.create_superuser(email="super@user.com", password="foo")
#         self.assertEqual(admin_user.email, "super@user.com")
#         self.assertTrue(admin_user.is_active)
#         self.assertTrue(admin_user.is_staff)
#         self.assertTrue(admin_user.is_superuser)
#         try:
#             # username is None for the AbstractUser option
#             # username does not exist for the AbstractBaseUser option
#             self.assertIsNone(admin_user.username)
#         except AttributeError:
#             pass
#         with self.assertRaises(ValueError):
#             User.objects.create_superuser(
#                 email="super@user.com", password="foo", is_superuser=False)

#     def test_create_superuser_with_number(self):
#         User = get_user_model()
#         admin_user = User.objects.create_superuser(phone_number="+233 50 457 2087", password="foo")
        
#         self.assertEqual(admin_user.phone_number, "+233 50 457 2087")
#         self.assertTrue(admin_user.is_active)
#         self.assertTrue(admin_user.is_staff)
#         self.assertTrue(admin_user.is_superuser)
        
#         try:
#             # username is None for the AbstractUser option
#             # username does not exist for the AbstractBaseUser option
#             self.assertIsNone(admin_user.username)
#         except AttributeError:
#             pass
        
#         with self.assertRaises(ValueError):
#             User.objects.create_superuser(
#                 phone_number="+233 50 457 2087", password="foo", is_superuser=False
#             )

from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth.models import Group
from rest_framework import status
from unittest.mock import MagicMock, patch
from users.models import CustomUser  # replace with your app name
from phonenumber_field.phonenumber import PhoneNumber


# class UserCreateTests(APITestCase):
#     def setUp(self):
#         # Create necessary groups
#         Group.objects.create(name="doctor")
#         Group.objects.create(name="healthworker")
#         Group.objects.create(name="driver")
#         Group.objects.create(name="individual")
#         Group.objects.create(name="health_admin")
#         Group.objects.create(name="driver_admin")
#         Group.objects.create(name="admin_driver")

#         self.url = reverse("register")
#         self.valid_data = {
#             "email": "testuser@example.com",  # Only email provided
#             "password": "securePassword123",
#             "first_name": "Test",
#             "last_name": "User",
#             "role": "Doctor",
#         }

#     @patch("users.views.send_token")  # Replace with actual import path
#     def test_user_creation_with_valid_data(self, mock_send_token):
#         mock_send_token.return_value = {"message": "Token sent successfully"}
#         data = self.valid_data.copy()

#         response = self.client.post(self.url, data, format="json")

#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertIn("user", response.data)
#         self.assertEqual(response.data["user"]["email"], data["email"])

#         user = CustomUser.objects.get(email=data["email"])
#         self.assertTrue(user.check_password(data["password"]))
#         self.assertEqual(user.role, "Doctor")
#         self.assertTrue(user.groups.filter(name="healthworker").exists())
#         mock_send_token.assert_called_once()

#     def test_user_creation_with_phone_only(self):
#         data = {
#             "phone_number": "+233541234567",
#             "password": "securePassword123",
#             "first_name": "Test",
#             "last_name": "User",
#             "role": "Driver",
#         }

#         response = self.client.post(self.url, data, format="json")

#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertIn("user", response.data)
#         user = CustomUser.objects.get(phone_number=data["phone_number"])
#         self.assertTrue(user.check_password(data["password"]))
#         self.assertEqual(user.role, "Driver")
#         self.assertTrue(user.groups.filter(name="driver").exists())

#     def test_missing_password_should_return_error(self):
#         data = self.valid_data.copy()
#         data.pop("password")

#         response = self.client.post(self.url, data, format="json")

#         self.assertEqual(response.status_code, 400)
#         self.assertIn("error", response.data)
#         self.assertEqual(response.data["error"], "no password found")

#     def test_invalid_role_should_return_error(self):
#         data = self.valid_data.copy()
#         data["role"] = "Alien"

#         response = self.client.post(self.url, data, format="json")

#         self.assertEqual(response.status_code, 400)
#         self.assertIn("error", response.data)

#     def test_email_and_phone_both_provided_should_return_error(self):
#         data = self.valid_data.copy()
#         data["phone_number"] = "+233541234567"  # Adding phone to existing email

#         response = self.client.post(self.url, data, format="json")

#         self.assertEqual(response.status_code, 400)
#         self.assertIn("error", response.data)

#     def test_neither_email_nor_phone_provided(self):
#         data = self.valid_data.copy()
#         data["email"] = ""
#         data["phone_number"] = ""

#         response = self.client.post(self.url, data, format="json")

#         self.assertEqual(response.status_code, 400)
#         self.assertIn("error", response.data)


class VerifyEmailViewTests(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(
            email="verifyme@example.com",
            password="securePassword123",
            role="Individual",
            email_verified=False
        )
        self.token = "valid-token"
        self.url = reverse("verify-email")  # Make sure your URL is named correctly

    @patch("users.views.OTPVerification.verify_otp")  # Patch the OTP verification method
    def test_verify_email_successful(self, mock_verify_otp):
        # Simulate valid OTP object returned with user
        mock_otp = MagicMock()
        mock_otp.user = self.user
        mock_verify_otp.return_value = mock_otp

        response = self.client.post(self.url, {"token": self.token}, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Email verified successfully")

        # Refresh user from DB and check email_verified is True
        self.user.refresh_from_db()
        self.assertTrue(self.user.email_verified)

    @patch("users.views.OTPVerification.verify_otp")
    def test_verify_email_invalid_token(self, mock_verify_otp):
        # Simulate invalid token (None returned)
        mock_verify_otp.return_value = None

        response = self.client.post(self.url, {"token": "invalid-token"}, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["message"], "Incorrect token")

    @patch("users.views.OTPVerification.verify_otp")
    def test_verify_email_exception_handling(self, mock_verify_otp):
        # Simulate exception being raised (e.g., decoding error)
        mock_verify_otp.side_effect = Exception("Token decoding failed")

        response = self.client.post(self.url, {"token": "any-token"}, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)
        self.assertEqual(response.data["error"], "Token decoding failed")


from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from unittest.mock import patch
from django.db.models import Q


class RequestVerificationCodeTests(APITestCase):
    def setUp(self):
        self.email_user = CustomUser.objects.create(
            email="emailuser@example.com",
            password="securePassword123",
            role="Individual",
        )

        self.phone_user = CustomUser.objects.create(
            phone_number="+233541234567",
            password="securePassword123",
            role="Driver",
        )

        self.url = reverse("verify-email")  # Ensure your URL is named correctly in urls.py

    @patch("users.views.send_token")  # Adjust this import to the actual path
    def test_send_verification_to_email_user(self, mock_send_token):
        mock_send_token.return_value = {"message": "Token sent via email"}

        response = self.client.post(self.url, {"username": self.email_user.email}, format="json")

        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertIn("token_info", response.data)
        self.assertEqual(response.data["token_info"]["message"], "Token sent via email")

        mock_send_token.assert_called_once_with(self.email_user, "email")

    # @patch("users.views.send_token")
    # def test_send_verification_to_phone_user(self, mock_send_token):
    #     mock_send_token.return_value = {"message": "Token sent via SMS"}

    #     response = self.client.post(self.url, {"username": str(self.phone_user.phone_number)}, format="json")

    #     self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
    #     self.assertIn("token_info", response.data)
    #     self.assertEqual(response.data["token_info"]["message"], "Token sent via SMS")

    #     mock_send_token.assert_called_once_with(self.phone_user, "sms")

    # def test_user_does_not_exist(self):
    #     response = self.client.post(self.url, {"username": "ghost@example.com"}, format="json")

    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    #     self.assertEqual(response.data["details"], "No such user")

