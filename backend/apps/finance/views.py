from django.shortcuts import render
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action

from .models import CuentaCorriente, Concepto, Movimiento, Pago
from .serializers import (
    CuentaCorrienteSerializer, ConceptoSerializer,
    MovimientoSerializer, PagoSerializer
)

#------------------------------
# ViewSets de Finanzas
#------------------------------
class CuentaCorrienteViewSet(viewsets.ModelViewSet):
    queryset = CuentaCorriente.objects.select_related("unidad").all()
    serializer_class = CuentaCorrienteSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=["get"])
    def estado(self, request, pk=None):
        cuenta = self.get_object()
        movimientos = cuenta.movimientos.all().order_by("-created_at")
        pagos = cuenta.pagos.all().order_by("-pagado_en")
        return Response({
            "unidad": cuenta.unidad.codigo,
            "saldo": cuenta.saldo_actual,
            "movimientos": MovimientoSerializer(movimientos, many=True).data,
            "pagos": PagoSerializer(pagos, many=True).data
        })

#------------------------------
# ViewSets de Movimientos y Pagos
#------------------------------
class ConceptoViewSet(viewsets.ModelViewSet):
    queryset = Concepto.objects.all()
    serializer_class = ConceptoSerializer
    permission_classes = [permissions.IsAuthenticated]

#------------------------------
# ViewSets de Movimientos y Pagos
#------------------------------
class MovimientoViewSet(viewsets.ModelViewSet):
    queryset = Movimiento.objects.select_related("cuenta", "concepto").all()
    serializer_class = MovimientoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        movimiento = serializer.save()
        # Actualizar saldo
        cuenta = movimiento.cuenta
        cuenta.saldo_actual += movimiento.debe
        cuenta.saldo_actual -= movimiento.haber
        cuenta.save()

#------------------------------
# ViewSets de Movimientos y Pagos
#------------------------------
class PagoViewSet(viewsets.ModelViewSet):
    queryset = Pago.objects.select_related("cuenta").all()
    serializer_class = PagoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        pago = serializer.save()
        # Actualizar saldo de la cuenta
        if pago.estado == Pago.Estado.EXITOSO:
            cuenta = pago.cuenta
            cuenta.saldo_actual -= pago.monto
            cuenta.save()
