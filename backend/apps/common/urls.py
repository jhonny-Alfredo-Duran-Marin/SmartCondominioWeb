from rest_framework.routers import DefaultRouter
from .views import PropiedadViewSet, OcupacionViewSet, EstablecimientoViewSet


router = DefaultRouter()
router.register("propiedades", PropiedadViewSet, basename="propiedades")
router.register("ocupaciones", OcupacionViewSet, basename="ocupaciones")
router.register("establecimientos", EstablecimientoViewSet, basename="establecimientos")

urlpatterns = router.urls

