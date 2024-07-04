from rest_framework import serializers
from .models import User
from django.contrib.auth import authenticate

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username','email', 'password', 'role')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data['email'],
            role='seller'  # Default role
        )
        return user

# class CustomAuthTokenSerializer(serializers.Serializer):
#     username = serializers.CharField(label="Username")
#     password = serializers.CharField(
#         label="Password",
#         style={'input_type': 'password'},
#         trim_whitespace=False
#     )

#     def validate(self, attrs):
#         username = attrs.get('username')
#         password = attrs.get('password')

#         if username and password:
#             user = authenticate(request=self.context.get('request'),
#                                 username=username, password=password)

#             if not user:
#                 raise serializers.ValidationError('Unable to log in with provided credentials.')

#         else:
#             raise serializers.ValidationError('Must include "username" and "password".')

#         attrs['user'] = user
#         return attrs


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'role']