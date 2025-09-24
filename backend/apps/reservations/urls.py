from rest_framework.routers import DefaultRouter
from .views import AreaComunViewSet, TarifaAreaViewSet, ReservaViewSet

router = DefaultRouter()
router.register("areas", AreaComunViewSet, basename="areas")
router.register("tarifas", TarifaAreaViewSet, basename="tarifas")
router.register("reservas", ReservaViewSet, basename="reservas")

urlpatterns = router.urls
