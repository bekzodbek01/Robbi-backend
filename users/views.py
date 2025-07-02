from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import EmailVerificationCode
from .serializers import *
from .utils import send_verification_code
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated


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

            # ✅ fullname ni ham saqlaymiz
            EmailVerificationCode.objects.create(
                email=email,
                code=code,
                fullname=fullname
            )

            return Response({'detail': 'Tasdiqlash kodi yuborildi.'})
        return Response(serializer.errors, status=400)



class RegisterVerifyView(APIView):
    def post(self, request):
        serializer = RegisterVerifySerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            code = serializer.validated_data['code']

            try:
                # ❌ get() o‘rniga ✅ filter().order_by('-created_at').first()
                code_obj = EmailVerificationCode.objects.filter(
                    email=email, code=code, is_used=False
                ).order_by('-created_at').first()

                if not code_obj:
                    return Response({'detail': 'Kod topilmadi yoki allaqachon ishlatilgan.'}, status=400)

                if code_obj.is_expired():
                    return Response({'detail': 'Kod eskirgan.'}, status=400)

                code_obj.is_used = True
                code_obj.save()

                fullname = code_obj.fullname or email.split('@')[0]

                user = User.objects.create_user(fullname=fullname, email=email)
                user.is_active = True
                user.save()

                refresh = RefreshToken.for_user(user)
                return Response({
                    'access': str(refresh.access_token),
                    'refresh': str(refresh)
                })

            except Exception as e:
                return Response({'detail': str(e)}, status=500)

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
                return Response({'detail': 'Noto‘g‘ri kod.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=400)


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserProfileSerializer(request.user, context={'request': request})
        return Response(serializer.data)

    def put(self, request):
        serializer = UserProfileSerializer(request.user, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)