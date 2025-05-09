from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import CustomUser
from .serializers import UserSerializer, HealthWorkerProfile, IndividualProfile
from django.db.models import Q
from rest_framework import status
from .models import OTPVerification
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import Group
import pyotp


class UserCreateAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():

            validated_data = serializer.validated_data.copy()
            password = request.data.get("password")
            if 'password' in validated_data:
                validated_data.pop('password')

            user = serializer.save()
            if password:
                user.set_password(password)
                user.save()

            role = request.data.get("role")
            # Validate role against a predefined list
            valid_roles = ["Doctor", "Nurse", "Org_Admin", "Individual", "Driver"]
            if role not in valid_roles:
                print("error here")
                return Response({"error": "Invalid role"}, status=status.HTTP_400_BAD_REQUEST)

            try:
                if role in ["Doctor", "Nurse"]:
                    health_workers = Group.objects.get(name="health_workers")
                    health_workers.user_set.add(user)
                    HealthWorkerProfile.objects.create(user=user)
                elif role == "Org_Admin":
                    admins = Group.objects.get(name="admins")
                    admins.user_set.add(user)
                    HealthWorkerProfile.objects.create(user=user)
                elif role == "Individual":
                    individuals = Group.objects.get(name="individuals")
                    individuals.user_set.add(user)
                    IndividualProfile.objects.create(user=user)
                elif role == "Driver":
                    drivers = Group.objects.get(name="drivers")
                    drivers.user_set.add(user)
                    IndividualProfile.objects.create(user=user)
            except Group.DoesNotExist:
                return Response({"error": f"Group for role {role} does not exist"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            try:
                if user.email:
                    info = send_token(user, method="Email")
                else:
                    info = send_token(user, method="SMS")
            except Exception as e:
                return Response({"error": f"Token generation failed: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            return Response({
                            "details": "user created successfully", 
                            "user" : UserSerializer(user).data,
                             "token_info": info
                            }, status=status.HTTP_201_CREATED)
        else:
            return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        try:
            user = CustomUser.objects.get(Q(email=username) | Q(phone_number=username))
            if user.check_password(password):
                # Check verification status
                if not (user.email_verified or user.phone_verified):
                    return Response(
                        {'error': 'Please verify your email or phone number before logging in'
                        },
                        status=status.HTTP_403_FORBIDDEN
                    )
            # get jwt token
                refresh = RefreshToken.for_user(user)
                return Response({'details': {
                                "Message": "Login successful",
                                },
                                 "access" : str(refresh.access_token),
                                 "refresh" : str(refresh)
                                }, status=status.HTTP_200_OK)
            
        except CustomUser.DoesNotExist:
            pass
        
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

class VerifyEmailView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        token = request.data.get('token')
        try:
            otp = OTPVerification.verify_otp(token)
            if otp is not None:
                otp.user.email_verified = True
                otp.user.save()
                return Response({'message': 'Email verified successfully'}, status=status.HTTP_200_OK)
            else:
                return Response({"message" : "Incorrect token"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': f'{str(e)}'}, status=status.HTTP_400_BAD_REQUEST)

class RequestVerificationCode(APIView):

    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        try:
            user = CustomUser.objects.get(Q(email=username) | Q(phone_number=username))
            if user.email:
                token_info = send_token(user, "email")
                print("Method : email")
            else:
                token_info = send_token(user, "sms")
                print("Method : sms")

            return Response({
                    "token_info" : token_info
                    }, 
                    status=status.HTTP_202_ACCEPTED
            )
        except CustomUser.DoesNotExist:
            pass
            
        return Response({"details" : "No such user"}, status=status.HTTP_400_BAD_REQUEST)
        
def send_token(user, method):
    otp = OTPVerification.objects.create(
        user=user, 
        secret_key = pyotp.random_base32(),
        method = method
    )
    otp.save()
    token = otp.generate_otp()

    return {
        "user" : str(user),
        "token" : token,
        "method" : method
    }

