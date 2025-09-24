from rest_framework import viewsets, permissions
from .models import Aviso, PushToken
from .serializers import AvisoSerializer, PushTokenSerializer


class AvisoViewSet(viewsets.ModelViewSet):
    queryset = Aviso.objects.all().order_by("-publicado_en")
    serializer_class = AvisoSerializer
    permission_classes = [permissions.IsAuthenticated]


class PushTokenViewSet(viewsets.ModelViewSet):
    queryset = PushToken.objects.all()
    serializer_class = PushTokenSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # Guarda el token asociado al usuario logueado
        serializer.save(usuario=self.request.user)
