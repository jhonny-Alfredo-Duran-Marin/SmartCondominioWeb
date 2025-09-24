from rest_framework.routers import DefaultRouter
from .views import CuentaCorrienteViewSet, ConceptoViewSet, MovimientoViewSet, PagoViewSet

router = DefaultRouter()
router.register("cuentas", CuentaCorrienteViewSet, basename="cuentas")
router.register("conceptos", ConceptoViewSet, basename="conceptos")
router.register("movimientos", MovimientoViewSet, basename="movimientos")
router.register("pagos", PagoViewSet, basename="pagos")

urlpatterns = router.urls
