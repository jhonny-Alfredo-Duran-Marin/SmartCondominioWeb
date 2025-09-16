from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import GroupViewSet, PermissionViewSet

router = DefaultRouter()
router.register('roles', GroupViewSet, basename='roles')
router.register('permissions', PermissionViewSet, basename='permissions')
urlpatterns = [path("", include(router.urls))]