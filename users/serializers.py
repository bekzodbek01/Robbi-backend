from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import EmailVerificationCode

User = get_user_model()


class RegisterSerializer(serializers.Serializer):
    fullname = serializers.CharField()
    email = serializers.EmailField()

class RegisterVerifySerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(max_length=6)


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()


class LoginVerifySerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(max_length=6)
