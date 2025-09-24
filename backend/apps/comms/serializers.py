from rest_framework import serializers
from .models import  PushToken, Aviso
class AvisoSerializer(serializers.ModelSerializer):
    publicado_por_nombre = serializers.CharField(source="publicado_por.correo", read_only=True)

    class Meta:
        model = Aviso
        fields = "__all__"


class PushTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = PushToken
        fields = "__all__"
