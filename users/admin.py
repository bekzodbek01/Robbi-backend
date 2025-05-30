from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, EmailVerificationCode

#
# @admin.register(User)
# class UserAdmin(BaseUserAdmin):
#     model = User
#     list_display = ('fullname', 'email', 'is_active', 'is_staff')
#     list_filter = ('is_active', 'is_staff')
#     search_fields = ('fullname', 'email')
#     ordering = ('date_joined',)
#
#     fieldsets = (
#         (None, {'fields': ('fullname', 'email', 'password')}),
#         ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
#         ('Important dates', {'fields': ('last_login', 'date_joined')}),
#         ('Groups & Permissions', {'fields': ('groups', 'user_permissions')}),
#     )
#
#     add_fieldsets = (
#         (None, {
#             'classes': ('wide',),
#             'fields': ('fullname', 'email', 'password1', 'password2', 'is_active', 'is_staff', 'is_superuser')}
#         ),
#     )


class UserAdmin(BaseUserAdmin):
    model = User
    list_display = ('id', 'fullname', 'lastname', 'email', 'is_active', 'is_staff')
    list_filter = ('is_active', 'is_staff')
    fieldsets = (
        (None, {'fields': ('fullname', 'lastname', 'email', 'password', 'image')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('fullname', 'lastname', 'email', 'password1', 'password2', 'is_active', 'is_staff')}
        ),
    )
    search_fields = ('fullname', 'email')
    ordering = ('id',)


admin.site.register(User, UserAdmin)
admin.site.register(EmailVerificationCode)
