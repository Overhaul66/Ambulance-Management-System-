from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import CustomUser
from .serializers import UserSerializer
from django.db.models import Q
from rest_framework import status
from .models import OTPVerification
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import Group
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from django.shortcuts import get_object_or_404
import pyotp



class UserCreateAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        password = request.data.pop('password', None)
        if not password:
            return Response({"error":"no password found"}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = UserSerializer(data=request.data,  context={'request': request})
        print(request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.set_password(password)
            user.save()
            

            # role = request.data.get("role")
            # # Validate role against a predefined list
            # valid_roles = ["Doctor", "Org_Admin", "Individual", "Driver"]
            # if role not in valid_roles:
            #     print("error here")
            #     return Response({"error": "Invalid role"}, status=status.HTTP_400_BAD_REQUEST)

            # try:
            #     if role == "Doctor":
            #         health_workers = Group.objects.get(name="health_workers")
            #         health_workers.user_set.add(user)
            #     elif role == "Org_Admin":
            #         admins = Group.objects.get(name="admins")
            #         admins.user_set(user)
            #         OrgAdminProfile.objects.create(user=user, organization=organization)
            #     elif role == "Individual":
            #         individuals = Group.objects.get(name="individuals")
            #         individuals.user_set.add(user)
            #     elif role == "Driver":
            #         drivers = Group.objects.get(name="drivers")
            #         drivers.user_set.add(user)
                   
            # except Group.DoesNotExist:
            #     return Response({"error": f"Group for role {role} does not exist"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            try:
                if user.email:
                    info = send_token(user, method="Email")
                else:
                    info = send_token(user, method="SMS")
                print(info)
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
                                 "user_role" : user.role,
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

class ManageUsersView(APIView):

    def get_queryset(self):
        return CustomUser.objects.all()
    # set permisions for methods
    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAuthenticated(), DjangoModelPermissions()]
        elif self.request.method == 'POST':
            return [IsAuthenticated(), DjangoModelPermissions()]  # or your JWT auth permission class
        elif self.request.method == 'DELETE':
            return [IsAuthenticated(), DjangoModelPermissions()]
        return [IsAuthenticated()]  # default fallback

    def get_authenticators(self):
        if self.request.method == 'GET':
            return [JWTAuthentication()]  
        elif self.request.method == 'POST':
            return [JWTAuthentication()]  # JWT auth for POST
        elif self.request.method == 'DELETE':
            return [JWTAuthentication()]
        return super().get_authenticators()

   
    def get(self, request):
        user = request.user
        group = user.groups.first()
        
        if group:
            if user.groups.filter(name__in=['health_admin', 'driver_admin']).exists():
                org_users = CustomUser.objects.filter(
                                organization=user.organization
                    )
                serializer = UserSerializer(org_users, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)

        return Response({"error":"you ain't part of this organization"},status=status.HTTP_403_FORBIDDEN)

    def post(self, request):

        serializer = UserSerializer(data=request.data, context={"request":request})
        if serializer.is_valid():
            user = serializer.save()
            user.email_verified = True # or user.phone_verified depending on the used format
            user.organization = request.user.organization
            user.save()
            return Response({"user":serializer.data, "detail":"user created successfully"},status=status.HTTP_202_ACCEPTED)
        
        return Response(serializer.errors,status=status.HTTP_403_FORBIDDEN)

    def delete(self, request):
        # either number or email
        username = request.data.pop('username', None)
        if not username:
            return Response({"error":"no username specified"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = get_object_or_404(CustomUser, Q(email=username) | Q(phone_number=username))
                
            user.delete()
            return Response(status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': f'{e}'}, status=status.HTTP_403_FORBIDDEN)
      
        
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




