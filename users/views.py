from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import EmailVerificationCode
from .serializers import *
from .utils import send_verification_code
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            fullname = serializer.validated_data['fullname']
            email = serializer.validated_data['email']
            if User.objects.filter(email=email).exists():
                return Response({'detail': 'Bu email allaqachon ro‘yxatdan o‘tgan.'}, status=400)

            EmailVerificationCode.objects.filter(email=email).delete()
            code = send_verification_code(email)
            return Response({'detail': 'Tasdiqlash kodi yuborildi.'})
        return Response(serializer.errors, status=400)


class RegisterVerifyView(APIView):
    def post(self, request):
        serializer = RegisterVerifySerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            code = serializer.validated_data['code']
            try:
                code_obj = EmailVerificationCode.objects.get(email=email, code=code, is_used=False)
                if code_obj.is_expired():
                    return Response({'detail': 'Kod eskirgan.'}, status=400)
                code_obj.is_used = True
                code_obj.save()

                fullname = request.data.get('fullname', email.split('@')[0])
                user = User.objects.create_user(fullname=fullname, email=email)
                user.is_active = True
                user.save()

                refresh = RefreshToken.for_user(user)
                return Response({
                    'access': str(refresh.access_token),
                    'refresh': str(refresh)
                })
            except EmailVerificationCode.DoesNotExist:
                return Response({'detail': 'Noto‘g‘ri kod.'}, status=400)
        return Response(serializer.errors, status=400)


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return Response({'detail': 'Iltimos, avval ro‘yxatdan o‘ting.'}, status=400)

            EmailVerificationCode.objects.filter(email=email).delete()
            send_verification_code(email)
            return Response({'detail': 'Tasdiqlash kodi yuborildi.'})
        return Response(serializer.errors, status=400)


class LoginVerifyView(APIView):
    def post(self, request):
        serializer = LoginVerifySerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            code = serializer.validated_data['code']
            try:
                code_obj = EmailVerificationCode.objects.get(email=email, code=code, is_used=False)
                if code_obj.is_expired():
                    return Response({'detail': 'Kod eskirgan.'}, status=400)
                code_obj.is_used = True
                code_obj.save()

                user = User.objects.get(email=email)
                refresh = RefreshToken.for_user(user)
                return Response({
                    'access': str(refresh.access_token),
                    'refresh': str(refresh)
                })
            except EmailVerificationCode.DoesNotExist:
                return Response({'detail': 'Noto‘g‘ri kod.'}, status=400)
        return Response(serializer.errors, status=400)
