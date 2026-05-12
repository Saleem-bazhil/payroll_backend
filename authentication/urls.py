from django.urls import path
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)
from .views import RoleTokenObtainPairView

urlpatterns = [
    path("login/", RoleTokenObtainPairView.as_view()),
    path("refresh/", TokenRefreshView.as_view()),
]
