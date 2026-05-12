from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)
from .views import RoleTokenObtainPairView
from .user_management_views import UserManagementViewSet

router = DefaultRouter()
router.register("users", UserManagementViewSet, basename="user-management")

urlpatterns = [
    path("login/", RoleTokenObtainPairView.as_view()),
    path("refresh/", TokenRefreshView.as_view()),
    path("", include(router.urls)),
]
