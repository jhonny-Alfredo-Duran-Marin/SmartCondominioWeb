from django.shortcuts import render
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from apps.comms.utils import enviar_notificacion_push

from .models import Condominio, Bloque, Unidad, Activo, OrdenTrabajo, Tarea,SeguimientoTarea
from .serializers import CondominioSerializer, BloqueSerializer, UnidadSerializer, ActivoSerializer,OrdenTrabajoSerializer, TareaSerializer,SeguimientoTareaSerializer

#-------------------------------
# ViewSets para la gestión de condominios, bloques, unidades y activos
#-------------------------------
class CondominioViewSet(viewsets.ModelViewSet):
    queryset = Condominio.objects.all()
    serializer_class = CondominioSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_destroy(self, instance):
        if instance.bloques.exists() or instance.activos.exists():
            raise ValidationError("No se puede eliminar un condominio con bloques o activos asociados")
        instance.delete()

#-------------------------------
# ViewSets para la gestión de bloques, unidades y activos
#-------------------------------
class BloqueViewSet(viewsets.ModelViewSet):
    queryset = Bloque.objects.select_related("condominio").all()
    serializer_class = BloqueSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_destroy(self, instance):
        if instance.unidades.exists():
            raise ValidationError("No se puede eliminar un bloque con unidades registradas")
        instance.delete()

#-------------------------------
# ViewSets para la gestión de unidades y activos
#-------------------------------
class UnidadViewSet(viewsets.ModelViewSet):
    queryset = Unidad.objects.select_related("bloque").all()
    serializer_class = UnidadSerializer
    permission_classes = [permissions.IsAuthenticated]

#-------------------------------
# ViewSets para la gestión de activos
#-------------------------------
class ActivoViewSet(viewsets.ModelViewSet):
    queryset = Activo.objects.select_related("condominio").all()
    serializer_class = ActivoSerializer
    permission_classes = [permissions.IsAuthenticated]

#-------------------------------
# ViewSets para la gestión de órdenes de trabajo y tareas
#-------------------------------
class OrdenTrabajoViewSet(viewsets.ModelViewSet):
    queryset = OrdenTrabajo.objects.select_related("activo", "solicitante").all()
    serializer_class = OrdenTrabajoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        """Si es un residente, guarda como solicitante"""
        persona = getattr(self.request.user, "persona", None)
        serializer.save(solicitante=persona)

    @action(detail=True, methods=["post"], permission_classes=[permissions.IsAdminUser])
    def aprobar(self, request, pk=None):
        """Administrador aprueba la orden de trabajo"""
        orden = self.get_object()
        if orden.estado == OrdenTrabajo.Estado.SOLICITADO:
            orden.estado = OrdenTrabajo.Estado.ASIGNADO
            orden.save()
            return Response({"status": "Orden aprobada"})
        return Response({"error": "La orden no está en estado solicitado"}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["post"], permission_classes=[permissions.IsAdminUser])
    def rechazar(self, request, pk=None):
        """Administrador rechaza la orden de trabajo"""
        orden = self.get_object()
        if orden.estado == OrdenTrabajo.Estado.SOLICITADO:
            orden.estado = OrdenTrabajo.Estado.PENDIENTE
            orden.save()
            return Response({"status": "Orden rechazada"})
        return Response({"error": "La orden no está en estado solicitado"}, status=status.HTTP_400_BAD_REQUEST)

#-------------------------------
# ViewSets para la gestión de tareas dentro de órdenes de trabajo
#-------------------------------
class TareaViewSet(viewsets.ModelViewSet):
    queryset = Tarea.objects.select_related("orden", "asignado_a").all()
    serializer_class = TareaSerializer
    permission_classes = [permissions.IsAuthenticated]


#-------------------------------
# ViewSets para la gestión de seguimientos de tareas
#-------------------------------
class SeguimientoTareaViewSet(viewsets.ModelViewSet):
    queryset = SeguimientoTarea.objects.select_related("tarea").all()
    serializer_class = SeguimientoTareaSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        seguimiento = serializer.save(actualizado_por=self.request.user.personal)

        # Notificar cuando el estado cambie
        tarea = seguimiento.tarea
        orden = tarea.orden
        usuarios_destino = [orden.solicitante.user] if orden.solicitante else []

        for u in usuarios_destino:
            enviar_notificacion_push(
                usuario=u,
                titulo=f"Tarea {tarea.id} actualizada",
                cuerpo=f"Estado cambió a {seguimiento.estado_nuevo}"
            )
