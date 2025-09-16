from django.contrib.auth.models import Group, Permission
from rest_framework import serializers
from django.contrib.auth import get_user_model
from apps.common.models import Persona, Personal
#-------------------(CU2)----------------------
# Serializers para los modelos de autenticación y
#  autorización de Django
# Incluye usuarios, grupos y permisos
#----------------------------------------------
class PermissionSerializer(serializers.ModelSerializer):
    # Muestra también a qué app/modelo pertenece el permiso
    app_label = serializers.CharField(source="content_type.app_label", read_only=True)
    model     = serializers.CharField(source="content_type.model", read_only=True)

    class Meta:
        model  = Permission
        fields = ["id", "codename", "name", "app_label", "model"]

class GroupSerializer(serializers.ModelSerializer):
    # Acepta lista de IDs de permisos
    permissions = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Permission.objects.all(), required=False
    )

    class Meta:
        model  = Group
        fields = ["id", "name", "permissions"]

    def create(self, validated_data):
        perms = validated_data.pop("permissions", [])
        group = Group.objects.create(**validated_data)
        if perms:
            group.permissions.set(perms)
        return group

    def update(self, instance, validated_data):
        perms = validated_data.pop("permissions", None)
        instance.name = validated_data.get("name", instance.name)
        instance.save()
        if perms is not None:
            instance.permissions.set(perms)
        return instance

#-------------------(CU1)----------------------
# 
#----------------------------------------------
User = get_user_model()

# CRUD admin de usuarios
class UserSerializer(serializers.ModelSerializer):
    from django.contrib.auth.models import Group
    groups = serializers.PrimaryKeyRelatedField(many=True, queryset=Group.objects.all(), required=False)
    password = serializers.CharField(write_only=True, required=True, min_length=8)

    class Meta:
        model = User
        fields = [
            "id", "username", "email", "first_name", "last_name",
            "is_active", "is_staff", "groups", "password",
            "date_joined", "last_login",
        ]
        read_only_fields = ["date_joined", "last_login"]

    def create(self, validated):
        groups = validated.pop("groups", [])
        password = validated.pop("password")
        user = User.objects.create(**validated)
        user.set_password(password)
        user.save()
        if groups:
            user.groups.set(groups)
        return user

    def update(self, instance, validated):
        groups = validated.pop("groups", None)
        password = validated.pop("password", None)
        for k, v in validated.items():
            setattr(instance, k, v)
        if password:
            instance.set_password(password)
        instance.save()
        if groups is not None:
            instance.groups.set(groups)
        return instance

# REGISTRO de RESIDENTE (User + Persona)
class RegisterResdentesSerializer(serializers.ModelSerializer):
    # datos persona
      ci = serializers.CharField(write_only=True)
      telefono = serializers.CharField(write_only=True, required=False, allow_blank=True)
      nombres = serializers.CharField(write_only=True)
      apellidos = serializers.CharField(write_only=True)
      fecha_nacimiento = serializers.DateField(write_only=True, required=False, allow_null=True)

      class Meta:
          model = User
          fields = [
              "id", "username", "email", "first_name", "last_name",
              "password", "ci", "telefono", "nombres", "apellidos", "fecha_nacimiento"
          ]
          extra_kwargs = {
              "password": {"write_only": True, "min_length": 8}}

      def validate(self, attrs):
          username = attrs["username"]
          if User.objects.filter(username=username).exists():
              raise serializers.ValidationError(
                  {"username": "El nombre de usuario ya está en uso."})
          
          email = attrs["email"]
          if email and User.objects.filter(email=email).exists():
                raise serializers.ValidationError(
                    {"email": "El correo electrónico ya está en uso."})
          
          return attrs
      
      def create(self, data):
          #crear usuario
          password = data.pop("password")
          ci = data.pop("ci")
          telefono = data.pop("telefono")
          nombres = data.pop("nombres")
          apellidos = data.pop("apellidos")
          fecha_nacimiento = data.pop("fecha_nacimiento", None)

          user = User.objects.create(**data)
          user.set_password(password)
          user.is_active = True
          user.save()
          
          #si ya tiene perfil de personal no permitir (regla de necogio)
          if hasattr(user,"personal"):
              raise serializers.ValidationError(
                  {"user": "El usuario ya tiene un perfil de personal asociado."})
          
          Persona.objects.create(
              user=user, ci=ci, telefono=telefono,
              nombres=nombres, apellidos=apellidos,
              fecha_nacimiento=fecha_nacimiento
           )
          #asignar Rol