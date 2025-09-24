from django.shortcuts import render

from rest_framework import viewsets, permissions
from .models import AreaComun, TarifaArea, Reserva
from .serializers import AreaComunSerializer, TarifaAreaSerializer, ReservaSerializer

#------------------------------
# Vistas para la gestión de reservas de áreas comunes
#------------------------------
class AreaComunViewSet(viewsets.ModelViewSet):
    queryset = AreaComun.objects.all()
    serializer_class = AreaComunSerializer
    permission_classes = [permissions.IsAuthenticated]

#------------------------------
# Vistas para las tarifas de áreas comunes
#------------------------------
class TarifaAreaViewSet(viewsets.ModelViewSet):
    queryset = TarifaArea.objects.select_related("area").all()
    serializer_class = TarifaAreaSerializer
    permission_classes = [permissions.IsAuthenticated]

#------------------------------
# Vistas para las reservas de áreas comunes
#------------------------------
class ReservaViewSet(viewsets.ModelViewSet):
    queryset = Reserva.objects.select_related("persona", "area").all()
    serializer_class = ReservaSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        persona = self.request.user.persona  # Se asocia automáticamente el usuario logueado
        serializer.save(persona=persona)
