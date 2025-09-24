from rest_framework.routers import DefaultRouter
from .views import AvisoViewSet, PushTokenViewSet

router = DefaultRouter()
router.register("avisos", AvisoViewSet, basename="avisos")
router.register("tokens", PushTokenViewSet, basename="tokens")
urlpatterns = router.urls
