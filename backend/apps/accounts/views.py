from django.contrib.auth.models import Group, Permission
from django.db.models import Q
from rest_framework import viewsets, permissions, decorators, response

from .serializers import GroupSerializer, PermissionSerializer  # <-- NOMBRE CORRECTO

class IsStaff(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_staff)

class PermissionViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class   = PermissionSerializer
    permission_classes = [IsStaff]

    def get_queryset(self):
        qs = Permission.objects.select_related("content_type").order_by(
            "content_type__app_label", "codename"
        )
        app = self.request.query_params.get("app")
        q   = self.request.query_params.get("search")
        if app:
            qs = qs.filter(content_type__app_label__icontains=app)
        if q:
            qs = qs.filter(Q(name__icontains=q) | Q(codename__icontains=q))
        return qs

class GroupViewSet(viewsets.ModelViewSet):
    queryset           = Group.objects.all().order_by("name")
    serializer_class   = GroupSerializer
    permission_classes = [IsStaff]

    @decorators.action(detail=True, methods=["post"], url_path="set-permissions")
    def set_permissions(self, request, pk=None):
        group = self.get_object()
        ids = request.data.get("permissions", [])
        if not isinstance(ids, list):
            return response.Response({"detail": "permissions debe ser lista de ids"}, status=400)
        group.permissions.set(Permission.objects.filter(id__in=ids))
        return response.Response({"detail": "ok", "count": group.permissions.count()})
