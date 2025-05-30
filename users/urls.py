from django.urls import path
from .views import *

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('register/verify/', RegisterVerifyView.as_view()),
    path('login/', LoginView.as_view()),
    path('login/verify/', LoginVerifyView.as_view()),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
]
