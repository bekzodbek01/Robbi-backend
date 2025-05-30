import random
from django.core.mail import send_mail
from .models import EmailVerificationCode
from django.utils import timezone
from datetime import timedelta

def send_verification_code(email):
    # Eskirgan kodlarni o'chirish
    EmailVerificationCode.objects.filter(email=email, is_used=False, created_at__lt=timezone.now()-timedelta(minutes=5)).delete()

    # Mavjud va ishlatilmagan, eskirmagan kodlarni tekshirish
    active_code = EmailVerificationCode.objects.filter(email=email, is_used=False).first()
    if active_code:
        return active_code.code

    # Yangi kod yaratish va yuborish
    code = str(random.randint(100000, 999999))
    EmailVerificationCode.objects.create(email=email, code=code)
    send_mail(
        subject='Tasdiqlash kodi',
        message=f'Sizning tasdiqlash kodingiz: {code}',
        from_email=None,
        recipient_list=[email],
    )
    return code
