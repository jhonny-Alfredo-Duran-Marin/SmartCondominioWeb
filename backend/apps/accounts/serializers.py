from django.contrib.auth.models import Group, Permission
from rest_framework import serializers
from django.contrib.auth import get_user_model
from apps.accounts.models import Persona, Personal
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
    groups = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Group.objects.all(), required=False
    )
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


# --------- REGISTRO RESIDENTE (User + Persona) ----------
class RegisterResidentSerializer(serializers.ModelSerializer):
    # Datos Persona
    ci = serializers.CharField(write_only=True)
    nombres = serializers.CharField(write_only=True)
    apellidos = serializers.CharField(write_only=True)
    telefono = serializers.CharField(write_only=True, required=False, allow_blank=True)
    fecha_nacimiento = serializers.DateField(write_only=True, required=False, allow_null=True)
    tipo = serializers.ChoiceField(write_only=True, choices=Persona.Tipo.choices)
    jefe = serializers.PrimaryKeyRelatedField(
        write_only=True, queryset=Persona.objects.all(), required=False, allow_null=True
    )

    class Meta:
        model = User
        fields = [
            "username", "password", "email", "first_name", "last_name",
            "ci", "nombres", "apellidos", "telefono", "fecha_nacimiento",
            "tipo", "jefe",
        ]
        extra_kwargs = {"password": {"write_only": True, "min_length": 8}}

    def validate(self, attrs):
        if User.objects.filter(username=attrs["username"]).exists():
            raise serializers.ValidationError({"username": "Ya existe"})
        email = attrs.get("email")
        if email and User.objects.filter(email=email).exists():
            raise serializers.ValidationError({"email": "Ya está en uso"})
        return attrs

    def create(self, data):
        password = data.pop("password")
        ci = data.pop("ci")
        nombres = data.pop("nombres")
        apellidos = data.pop("apellidos")
        telefono = data.pop("telefono", "")
        fecha_nacimiento = data.pop("fecha_nacimiento", None)
        tipo = data.pop("tipo")
        jefe = data.pop("jefe", None)

        user = User.objects.create(**data, is_active=True)
        user.set_password(password)
        user.save()

        if hasattr(user, "personal"):
            raise serializers.ValidationError("El usuario ya es Personal.")

        persona = Persona.objects.create(
            user=user, ci=ci, nombres=nombres, apellidos=apellidos,
            telefono=telefono, fecha_nacimiento=fecha_nacimiento,
            tipo=tipo, jefe=jefe
        )

        # rol por defecto
        residente = Group.objects.filter(name="Residente").first()
        if residente:
            user.groups.add(residente)

        return user


# --------- ALTA PERSONAL (User + Personal, sólo admin) ----------
class CreateStaffSerializer(serializers.ModelSerializer):
    # Datos Personal (nota: nombre en singular)
    nombre = serializers.CharField(write_only=True)
    apellidos = serializers.CharField(write_only=True)
    cargo = serializers.CharField(write_only=True)
    estado = serializers.ChoiceField(write_only=True, choices=Personal.Estado.choices)
    fecha_contratacion = serializers.DateField(write_only=True)
    sueldo = serializers.DecimalField(write_only=True, max_digits=10, decimal_places=2)
    tipo = serializers.ChoiceField(write_only=True, choices=Personal.Tipo.choices)

    class Meta:
        model = User
        fields = [
            "username", "password", "email",
            "nombre", "apellidos", "cargo", "estado",
            "fecha_contratacion", "sueldo", "tipo",
        ]
        extra_kwargs = {"password": {"write_only": True, "min_length": 8}}

    def create(self, data):
        password = data.pop("password")

        nombre = data.pop("nombre")
        apellidos = data.pop("apellidos")
        cargo = data.pop("cargo")
        estado = data.pop("estado")
        fecha_contratacion = data.pop("fecha_contratacion")
        sueldo = data.pop("sueldo")
        tipo = data.pop("tipo")

        user = User.objects.create(**data, is_active=True, is_staff=True)
        user.set_password(password)
        user.save()

        if hasattr(user, "persona"):
            raise serializers.ValidationError("El usuario ya es Residente.")

        Personal.objects.create(
            user=user, nombre=nombre, apellidos=apellidos, cargo=cargo,
            estado=estado, fecha_contratacion=fecha_contratacion,
            sueldo=sueldo, tipo=tipo
        )

        personal_group = Group.objects.filter(name="Personal").first()
        if personal_group:
            user.groups.add(personal_group)

        return user