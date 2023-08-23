from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
# from .models import CustomUser
from .serializers import LoginSerializer, RegistrationSerializer, ChangePasswordSerializer, ProfileSerializer
from django.utils import timezone
# from rest_framework.generics import UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import authenticate
from .models import Profile


class RegistrationView(APIView):
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            username = serializer.validated_data.get('username')
            email = serializer.validated_data.get('email')
            profile = Profile(user=user, username=username, email=email)
            profile.save()


            refresh = RefreshToken.for_user(user)
            return Response(
                {
                    "user": serializer.data,
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                    'message': 'Registration successful'
                },
                status=status.HTTP_201_CREATED,
                headers={'Location': ''}
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





class LoginView(APIView):
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        
        # user = CustomUser.objects.filter(email=email).first()
        user = authenticate(email=email, password=password)

        if user:
            user.last_login = timezone.now()
            user.save()
            refresh = RefreshToken.for_user(user)
            return Response(
                {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                    'message': 'Authorization successful'
                },
                status=status.HTTP_200_OK,
            )
        return Response({"detail": "Invalid data"}, status=status.HTTP_400_BAD_REQUEST)





# class ChangePasswordView(UpdateAPIView):
#     serializer_class = ChangePasswordSerializer
#     permission_classes = [IsAuthenticated]

#     def get_object(self):
#         return self.request.user

#     def update(self, request, *args, **kwargs):
#         user = self.get_object()
#         serializer = self.get_serializer(data=request.data)

#         if serializer.is_valid():
#             if not user.check_password(serializer.validated_data["old_password"]):
#                 return Response({"old_password": ["Wrong password."]}, status=400)

#             user.set_password(serializer.validated_data["new_password"])
#             user.save()
#             return Response({"message": "Password successfully changed."}, status=200)

#         return Response(serializer.errors, status=400)



class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = Profile.objects.get(user=request.user)
        serializer = ProfileSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request):
        user_profile = Profile.objects.get(user=request.user)
        serializer = ProfileSerializer(user_profile, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        user = request.user
        serializer = ChangePasswordSerializer(data=request.data)

        if serializer.is_valid():
            if not user.check_password(serializer.validated_data["old_password"]):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)

            user.set_password(serializer.validated_data["new_password"])
            user.save()
            return Response({"message": "Password successfully changed."}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)