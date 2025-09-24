from rest_framework import serializers
from .models import Condominio, Bloque, Unidad, Activo,SeguimientoTarea
from .models import OrdenTrabajo, Tarea

#-------------------------------
# Serializers para la gestión de condominios, bloques, unidades y activos
#-------------------------------
class CondominioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Condominio
        fields = "__all__"

    def validate(self, data):
        if "ciudad" in data and not data["ciudad"].strip():
            raise serializers.ValidationError("La ciudad no puede estar vacía")
        return data

#-------------------------------
# Serializers para la gestión de bloques, unidades y activos
#-------------------------------
class BloqueSerializer(serializers.ModelSerializer):
    condominio_nombre = serializers.CharField(source="condominio.nombre", read_only=True)

    class Meta:
        model = Bloque
        fields = "__all__"

    def validate(self, data):
        condominio = data["condominio"]
        nombre = data["nombre"]
        if Bloque.objects.filter(condominio=condominio, nombre=nombre).exists():
            raise serializers.ValidationError("Ya existe un bloque con este nombre en el condominio")
        return data

#-------------------------------
# Serializers para la gestión de unidades y activos
#-------------------------------
class UnidadSerializer(serializers.ModelSerializer):
    bloque_nombre = serializers.CharField(source="bloque.nombre", read_only=True)

    class Meta:
        model = Unidad
        fields = "__all__"

    def validate_area(self, value):
        if value <= 0:
            raise serializers.ValidationError("El área debe ser mayor a 0")
        return value

    def validate_mantenimiento(self, value):
        if value < 0:
            raise serializers.ValidationError("El mantenimiento no puede ser negativo")
        return value

    def validate(self, data):
        bloque = data["bloque"]
        codigo = data["codigo"]
        if Unidad.objects.filter(bloque=bloque, codigo=codigo).exists():
            raise serializers.ValidationError("Ya existe una unidad con ese código en este bloque")
        return data

#-------------------------------
# Serializers para la gestión de activos
#-------------------------------
class ActivoSerializer(serializers.ModelSerializer):
    condominio_nombre = serializers.CharField(source="condominio.nombre", read_only=True)

    class Meta:
        model = Activo
        fields = "__all__"

    def validate(self, data):
        condominio = data["condominio"]
        nombre = data["nombre"]
        if Activo.objects.filter(condominio=condominio, nombre=nombre).exists():
            raise serializers.ValidationError("Ya existe un activo con este nombre en el condominio")
        return data

#-------------------------------
# Serializers para la gestión de órdenes de trabajo y tareas
#-------------------------------
class OrdenTrabajoSerializer(serializers.ModelSerializer):
    activo_nombre = serializers.CharField(source="activo.nombre", read_only=True)
    solicitante_nombre = serializers.CharField(source="solicitante.nombres", read_only=True)

    class Meta:
        model = OrdenTrabajo
        fields = "__all__"

#-------------------------------
# Serializers para la gestión de tareas dentro de órdenes de trabajo
#-------------------------------
class TareaSerializer(serializers.ModelSerializer):
    orden_titulo = serializers.CharField(source="orden.titulo", read_only=True)
    asignado_a_nombre = serializers.CharField(source="asignado_a.nombre", read_only=True)

    class Meta:
        model = Tarea
        fields = "__all__"

#-------------------------------
# Serializers para la gestión de seguimientos de tareas
#-------------------------------
class SeguimientoTareaSerializer(serializers.ModelSerializer):
    tarea_descripcion = serializers.CharField(source="tarea.descripcion", read_only=True)

    class Meta:
        model = SeguimientoTarea
        fields = "__all__"
