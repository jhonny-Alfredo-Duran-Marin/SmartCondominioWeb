from rest_framework import serializers
from .models import Propiedad, Ocupacion
from apps.maintenance.models import Unidad
from apps.accounts.models import Persona

# ------------------------------
# Serializers base
# ------------------------------

class PersonaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Persona
        fields = ["id", "nombres", "apellidos", "ci", "estado", "tipo"]


class UnidadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unidad
        fields = ["id", "codigo", "numero", "piso", "area", "estado"]


class PropiedadSerializer(serializers.ModelSerializer):
    persona = PersonaSerializer(read_only=True)

    class Meta:
        model = Propiedad
        fields = ["id", "tipo", "porcentaje", "fecha_inicio", "fecha_fin", "persona", "unidad"]


class OcupacionSerializer(serializers.ModelSerializer):
    persona = PersonaSerializer(read_only=True)

    class Meta:
        model = Ocupacion
        fields = ["id", "rol_hogar", "estado", "fecha_inicio", "fecha_fin", "persona", "unidad"]

# ------------------------------
# Serializer combinado: Establecimiento
# ------------------------------

class EstablecimientoSerializer(serializers.ModelSerializer):
    propietario = serializers.SerializerMethodField()
    ocupantes = serializers.SerializerMethodField()

    class Meta:
        model = Unidad
        fields = ["id", "codigo", "numero", "piso", "area", "estado", "propietario", "ocupantes"]

    def get_propietario(self, obj):
        propiedad = obj.propiedades.first()  # primera propiedad asociada a la unidad
        return PropiedadSerializer(propiedad).data if propiedad else None

    def get_ocupantes(self, obj):
        ocupaciones = obj.ocupantes.all()
        return OcupacionSerializer(ocupaciones, many=True).data
