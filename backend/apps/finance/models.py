from django.db import models

from apps.maintenance.models import Unidad

#------------------------------
# Modelos de Finanzas
#------------------------------
class CuentaCorriente(models.Model):
    unidad = models.OneToOneField(Unidad, on_delete=models.CASCADE, related_name="cuenta_corriente")
    saldo_actual = models.FloatField(default=0.0)

    def __str__(self):
        return f"Cuenta {self.unidad.codigo} - Saldo {self.saldo_actual} Bs."

#------------------------------
# Modelos de Movimientos y Pagos
#------------------------------
class Concepto(models.Model):
    class Tipo(models.TextChoices):
        CUOTA = "Cuota", "Cuota"
        EXPENSA = "Expensa", "Expensa"
        MULTA = "Multa", "Multa"
        OTRO = "Otro", "Otro"

    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    tipo = models.CharField(max_length=20, choices=Tipo.choices)

    def __str__(self):
        return f"{self.nombre} ({self.tipo})"

#------------------------------
# Modelos de Movimientos y Pagos
#------------------------------
class Movimiento(models.Model):
    cuenta = models.ForeignKey(CuentaCorriente, on_delete=models.CASCADE, related_name="movimientos")
    concepto = models.ForeignKey(Concepto, on_delete=models.CASCADE, related_name="movimientos")
    descripcion = models.TextField(blank=True)
    debe = models.FloatField(default=0.0)   # lo que se carga
    haber = models.FloatField(default=0.0)  # lo que se abona
    periodo = models.DateField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.concepto.nombre} - Debe: {self.debe} / Haber: {self.haber}"

#------------------------------
# Modelos de Movimientos y Pagos
#------------------------------
class Pago(models.Model):
    class Estado(models.TextChoices):
        EXITOSO = "Exitoso", "Exitoso"
        EN_PROCESO = "EnProceso", "En Proceso"
        RECHAZADO = "Rechazado", "Rechazado"

    class Metodo(models.TextChoices):
        QR = "QR", "QR"
        TRANSFERENCIA = "Transferencia", "Transferencia"
        EFECTIVO = "Efectivo", "Efectivo"

    cuenta = models.ForeignKey(CuentaCorriente, on_delete=models.CASCADE, related_name="pagos")
    comprobante = models.CharField(max_length=200)
    estado = models.CharField(max_length=20, choices=Estado.choices, default=Estado.EN_PROCESO)
    metodo = models.CharField(max_length=20, choices=Metodo.choices)
    monto = models.FloatField()
    pagado_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Pago {self.monto} Bs ({self.estado})"
