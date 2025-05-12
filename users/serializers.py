from rest_framework import serializers
from .models import User
import random

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email']

    def create(self, validated_data):
        email = validated_data['email']
        code = str(random.randint(100000, 999999))

        user, created = User.objects.get_or_create(email=email)
        user.verification_code = code
        user.is_active = False
        user.save()

        from django.core.mail import send_mail
        send_mail(
            "Tasdiqlash kodi",
            f"Sizning tasdiqlash kodingiz: {code}",
            'bekzodbek5201@gmail.com',
            [email],
        )

        return user

class VerifySerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(max_length=6)
