from rest_framework.routers import DefaultRouter
from .views import CondominioViewSet, BloqueViewSet, UnidadViewSet, ActivoViewSet, OrdenTrabajoViewSet, TareaViewSet,SeguimientoTareaViewSet

router = DefaultRouter()
router.register("condominios", CondominioViewSet, basename="condominios")
router.register("bloques", BloqueViewSet, basename="bloques")
router.register("unidades", UnidadViewSet, basename="unidades")
router.register("activos", ActivoViewSet, basename="activos")
router.register("ordenes", OrdenTrabajoViewSet, basename="ordenes")
router.register("tareas", TareaViewSet, basename="tareas")
router.register("seguimientos", SeguimientoTareaViewSet, basename="seguimientos")

urlpatterns = router.urls

