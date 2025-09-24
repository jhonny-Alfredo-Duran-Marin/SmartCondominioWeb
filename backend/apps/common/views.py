from rest_framework import viewsets
from .models import Propiedad, Ocupacion
from apps.maintenance.models import Unidad
from .serializers import PropiedadSerializer, OcupacionSerializer,EstablecimientoSerializer

# ------------------------------
# ViewSets para Propiedades y Ocupaciones
# ------------------------------
class PropiedadViewSet(viewsets.ModelViewSet):
    queryset = Propiedad.objects.all()
    serializer_class = PropiedadSerializer

# ------------------------------
# ViewSet para Ocupaciones
# ------------------------------
class OcupacionViewSet(viewsets.ModelViewSet):
    queryset = Ocupacion.objects.all()
    serializer_class = OcupacionSerializer

# ------------------------------
# ViewSet combinado: Establecimientos
# ------------------------------
class EstablecimientoViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Endpoint de solo lectura para listar establecimientos completos:
    Unidad + Propietario + Ocupantes
    """
    queryset = Unidad.objects.all()
    serializer_class = EstablecimientoSerializer
