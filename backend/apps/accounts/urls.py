from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    GroupViewSet, PermissionViewSet, UserViewSet,
    RegisterResidentView, CreateStaffView
)

router = DefaultRouter()
router.register("roles",       GroupViewSet,      basename="roles")
router.register("permissions", PermissionViewSet, basename="permissions")
router.register("users",       UserViewSet,       basename="users")

urlpatterns = [
    path("", include(router.urls)),

    # Endpoints CU1:
    path("register/", RegisterResidentView.as_view(), name="register-resident"),
    path("staff/",    CreateStaffView.as_view(),     name="create-staff"),
]
