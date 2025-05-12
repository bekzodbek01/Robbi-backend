import random
from django.core.mail import send_mail
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User, EmailVerificationCode
# Kod yuborish view


class RegisterView(APIView):
    def post(self, request):
        email = request.data.get("email")
        if not email:
            return Response({"error": "Email kiritilishi shart"}, status=400)

        # Foydalanuvchi mavjud bo'lmasa, yaratamiz
        user, _ = User.objects.get_or_create(email=email)

        # Avvalgi kodlarni bekor qilamiz
        EmailVerificationCode.objects.filter(email=email, is_used=False).update(is_used=True)

        # Yangi kod yaratamiz
        code = str(random.randint(100000, 999999))
        EmailVerificationCode.objects.create(email=email, code=code)

        try:
            send_mail(
                subject="Tasdiqlash kodingiz",
                message=f"Sizning tasdiqlash kodingiz: {code}",
                from_email="bekzodbek5201@gmail.com",
                recipient_list=[email],
                fail_silently=False,
            )
        except Exception as e:
            return Response({"error": f"Email yuborilmadi: {str(e)}"}, status=500)

        return Response({"message": f"{email} ga tasdiqlash kodi yuborildi."}, status=200)


class VerifyCodeView(APIView):
    def post(self, request):
        email = request.data.get("email")
        code = request.data.get("code")

        if not email or not code:
            return Response({"error": "Email va kod kiritilishi shart"}, status=400)

        verification = EmailVerificationCode.objects.filter(
            email=email, code=code, is_used=False
        ).first()

        if not verification:
            return Response({"error": "Kod noto‘g‘ri yoki allaqachon ishlatilgan."}, status=400)

        if verification.is_expired():
            return Response({"error": "Kod muddati tugagan (5 daqiqa)."}, status=400)

        # Kodni ishlatilgan deb belgilash
        verification.is_used = True
        verification.save()

        # Foydalanuvchini faollashtirish
        user = User.objects.get(email=email)
        user.is_active = True
        user.save()

        # JWT tokenlar yaratish
        refresh = RefreshToken.for_user(user)
        return Response({
            "access": str(refresh.access_token),
            "refresh": str(refresh)
        }, status=status.HTTP_200_OK)
