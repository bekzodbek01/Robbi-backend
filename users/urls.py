from django.urls import path
from .views import RegisterView, VerifyCodeView

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('verify/', VerifyCodeView.as_view()),
]
