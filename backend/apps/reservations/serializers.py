from rest_framework import serializers
from .models import AreaComun, TarifaArea, Reserva

#------------------------------
# Serializers para la gestión de reservas de áreas comunes
#------------------------------
class AreaComunSerializer(serializers.ModelSerializer):
    class Meta:
        model = AreaComun
        fields = "__all__"

#------------------------------
# Serializers para las tarifas de áreas comunes
#------------------------------
class TarifaAreaSerializer(serializers.ModelSerializer):
    area_nombre = serializers.CharField(source="area.nombre", read_only=True)

    class Meta:
        model = TarifaArea
        fields = "__all__"

#------------------------------
# Serializers para las reservas de áreas comunes
#------------------------------
class ReservaSerializer(serializers.ModelSerializer):
    persona_nombre = serializers.CharField(source="persona.nombres", read_only=True)
    area_nombre = serializers.CharField(source="area.nombre", read_only=True)

    class Meta:
        model = Reserva
        fields = "__all__"

    def validate(self, data):
        # Validar que hora_fin sea después de hora_inicio
        if data["hora_fin"] <= data["hora_inicio"]:
            raise serializers.ValidationError("La hora de fin debe ser mayor a la hora de inicio")

        # Validar que no haya solapamiento de reservas
        overlapping = Reserva.objects.filter(
            area=data["area"],
            fecha=data["fecha"],
            hora_inicio__lt=data["hora_fin"],
            hora_fin__gt=data["hora_inicio"],
        )
        if self.instance:
            overlapping = overlapping.exclude(id=self.instance.id)
        if overlapping.exists():
            raise serializers.ValidationError("Ya existe una reserva para este horario en el área seleccionada")

        return data
