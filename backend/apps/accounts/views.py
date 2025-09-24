from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework import status, viewsets, decorators, response
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from drf_spectacular.utils import extend_schema

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission

from .serializers import (
    GroupSerializer,
    PermissionSerializer,
    UserSerializer,
    RegisterResidentSerializer,
    CreateStaffSerializer,
)

User = get_user_model()

# ---------- Roles ----------
class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all().order_by("id")
    serializer_class = GroupSerializer
    permission_classes = [IsAdminUser]

# ---------- Permisos ----------
class PermissionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Permission.objects.all().order_by("id")
    serializer_class = PermissionSerializer
    permission_classes = [IsAdminUser]

# ---------- CRUD Usuarios (solo admin) ----------
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by("id")
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]

    @decorators.action(detail=True, methods=["post"], url_path="set-password")
    def set_password(self, request, pk=None):
        user = self.get_object()
        pwd = request.data.get("password", "")
        if len(pwd) < 8:
            return response.Response({"detail": "password demasiado corta (min 8)"}, status=400)
        user.set_password(pwd)
        user.save()
        return response.Response({"detail": "password actualizada"})

# ---------- Registro Residente (público) ----------
class RegisterResidentView(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = RegisterResidentSerializer

    @extend_schema(
        request=RegisterResidentSerializer,
        responses={201: UserSerializer},
        summary="Registrar residente (User + Persona)"
    )
    def post(self, request, *args, **kwargs):
        s = self.get_serializer(data=request.data)
        s.is_valid(raise_exception=True)
        user = s.save()

        refresh = RefreshToken.for_user(user)
        return Response({
            "user": UserSerializer(user).data,
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        }, status=status.HTTP_201_CREATED)

# ---------- Alta Personal (solo admin) ----------
class CreateStaffView(GenericAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = CreateStaffSerializer

    @extend_schema(
        request=CreateStaffSerializer,
        responses={201: UserSerializer},
        summary="Crear personal (User + Personal)"
    )
    def post(self, request, *args, **kwargs):
        s = self.get_serializer(data=request.data)
        s.is_valid(raise_exception=True)
        user = s.save()

        refresh = RefreshToken.for_user(user)
        return Response({
            "user": UserSerializer(user).data,
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        }, status=status.HTTP_201_CREATED)
