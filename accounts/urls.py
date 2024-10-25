# accounts/urls.py
from django.urls import path
from .views import UserCreateView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('register/', UserCreateView.as_view(), name='user-register'),  # Rota para registrar novos usuários
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # Rota para login e obtenção do token JWT
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Rota para atualizar o token JWT
]
