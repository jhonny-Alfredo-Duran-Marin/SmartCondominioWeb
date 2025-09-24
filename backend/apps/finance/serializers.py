from rest_framework import serializers
from .models import CuentaCorriente, Concepto, Movimiento, Pago

#------------------------------
# Serializers de Finanzas
#------------------------------
class CuentaCorrienteSerializer(serializers.ModelSerializer):
    unidad_codigo = serializers.CharField(source="unidad.codigo", read_only=True)

    class Meta:
        model = CuentaCorriente
        fields = "__all__"

#------------------------------
# Serializers de Movimientos y Pagos
#------------------------------
class ConceptoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Concepto
        fields = "__all__"

#------------------------------
# Serializers de Movimientos y Pagos
#------------------------------
class MovimientoSerializer(serializers.ModelSerializer):
    cuenta_unidad = serializers.CharField(source="cuenta.unidad.codigo", read_only=True)
    concepto_nombre = serializers.CharField(source="concepto.nombre", read_only=True)

    class Meta:
        model = Movimiento
        fields = "__all__"

#------------------------------
# Serializers de Movimientos y Pagos
#------------------------------
class PagoSerializer(serializers.ModelSerializer):
    cuenta_unidad = serializers.CharField(source="cuenta.unidad.codigo", read_only=True)

    class Meta:
        model = Pago
        fields = "__all__"
