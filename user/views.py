from django.shortcuts import render

# Create your views here.
# users/views.py

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import get_user_model
from .serializers import UserSerializer
from rest_framework.response import Response

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token

from rest_framework.views import APIView
from rest_framework import viewsets

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


# class CustomAuthToken(ObtainAuthToken):
#     serializer_class = CustomAuthTokenSerializer

#     def post(self, request, *args, **kwargs):
#         serializer = self.serializer_class(data=request.data, context={'request': request})
#         serializer.is_valid(raise_exception=True)
#         user = serializer.validated_data['user']
#         token, created = Token.objects.get_or_create(user=user)
#         return Response({
#             'token': token.key,
#             'user_id': user.pk,
#             'username': user.username,
#             'role': user.role  # Assuming user.role is a field in your user model
#         })

class CustomAuthToken(ObtainAuthToken):
    
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])
        return Response({
            'token': token.key,
            'user_id': token.user_id,
            'username': token.user.username,
            'role': token.user.role  # Assuming user.role is a field in your user model
        })

class ProfileView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
    


class UserListView(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            # Delete the token to log the user out
            request.user.auth_token.delete()
        except Exception as e:
            return Response({'error': str(e)}, status=400)
        return Response({'success': 'Logout successful'}, status=200)