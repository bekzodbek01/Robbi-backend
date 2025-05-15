# from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
# from django.db import models
# from django.utils import timezone
# from datetime import timedelta
#
#
# class EmailVerificationCode(models.Model):
#     email = models.EmailField()
#     code = models.CharField(max_length=6)
#     created_at = models.DateTimeField(auto_now_add=True)
#     is_used = models.BooleanField(default=False)
#
#     def is_expired(self):
#         return timezone.now() > self.created_at + timedelta(minutes=1)
#
#     def __str__(self):
#         return f"{self.email} - {self.code}"
#
#
# class UserManager(BaseUserManager):
#     def create_user(self, email, password=None, **extra_fields):
#         if not email:
#             raise ValueError("Email kiritilishi shart.")
#         email = self.normalize_email(email)
#         user = self.model(email=email, **extra_fields)
#         if password:
#             user.set_password(password)
#         else:
#             user.set_unusable_password()
#         user.save()
#         return user
#
#     def create_superuser(self, email, password, **extra_fields):
#         extra_fields.setdefault('is_staff', True)
#         extra_fields.setdefault('is_superuser', True)
#         extra_fields.setdefault('is_active', True)
#         return self.create_user(email, password, **extra_fields)
#
#
# class User(AbstractBaseUser, PermissionsMixin):
#     email = models.EmailField(unique=True)
#     is_active = models.BooleanField(default=False)
#     is_staff = models.BooleanField(default=False)
#
#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = []
#
#     objects = UserManager()
#
#     def __str__(self):
#         return self.email
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
from datetime import timedelta


class EmailVerificationCode(models.Model):
    email = models.EmailField()
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)

    def is_expired(self):
        return timezone.now() > self.created_at + timedelta(minutes=5)

    def __str__(self):
        return f"{self.email} - {self.code}"


class UserManager(BaseUserManager):
    def create_user(self, fullname, password=None, **extra_fields):
        if not fullname:
            raise ValueError("To‘liq ism (fullname) kiritilishi shart.")
        user = self.model(fullname=fullname, **extra_fields)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save()
        return user

    def create_superuser(self, fullname, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        return self.create_user(fullname=fullname, password=password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    fullname = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True, null=True, blank=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'fullname'
    REQUIRED_FIELDS = []  # superuser yaratishda faqat fullname va password talab qilinadi

    objects = UserManager()

    def __str__(self):
        return self.fullname
