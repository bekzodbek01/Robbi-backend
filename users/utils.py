import random
from django.core.mail import send_mail
from .models import EmailVerificationCode

def send_verification_code(email):
    code = str(random.randint(100000, 999999))
    EmailVerificationCode.objects.create(email=email, code=code)
    send_mail(
        subject='Tasdiqlash kodi',
        message=f'Sizning tasdiqlash kodingiz: {code}',
        from_email=None,
        recipient_list=[email],
    )
    return code
