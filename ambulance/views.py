from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import AmbulanceRequest
from .serializers import AmbulanceRequestSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated

# Create your views here.

class RequestRideView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # only individuals and health workers can request an ambulance
        if request.user.has_perm("request ambulance"):
            serializer = AmbulanceRequestSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(user=request.user)  # Assuming the user is authenticated
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"detail":"permission not allowed"}, status=status.HTTP_403_FORBIDDEN)
