from django.db import models
from django.conf import settings
from apps.accounts.models import Persona
from apps.maintenance.models import Condominio

#------------------------------
# Modelos para la gestión de reservas de áreas comunes
#------------------------------
class AreaComun(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    requiere_pago = models.BooleanField(default=False)
    condominio = models.ForeignKey(Condominio, on_delete=models.CASCADE, related_name="areas_comunes")

    def __str__(self):
        return f"{self.nombre} ({self.condominio.nombre})"

#------------------------------
# Tarifas para el uso de áreas comunes
#------------------------------
class TarifaArea(models.Model):
    area = models.ForeignKey(AreaComun, on_delete=models.CASCADE, related_name="tarifas")
    monto = models.FloatField()
    nombre = models.CharField(max_length=100)
    vigencia_inicio = models.DateField()
    vigencia_final = models.DateField()

    def __str__(self):
        return f"{self.nombre} - {self.monto} Bs."

#------------------------------
# Reservas de áreas comunes por parte de los residentes
#------------------------------
class Reserva(models.Model):
    class Estado(models.TextChoices):
        DISPONIBLE = "Disponible", "Disponible"
        OCUPADO = "Ocupado", "Ocupado"
        EN_USO = "EnUso", "En Uso"

    persona = models.ForeignKey(Persona, on_delete=models.CASCADE, related_name="reservas")
    area = models.ForeignKey(AreaComun, on_delete=models.CASCADE, related_name="reservas")

    comprobante_url = models.CharField(max_length=200, blank=True, null=True)
    estado = models.CharField(max_length=20, choices=Estado.choices, default=Estado.DISPONIBLE)
    fecha = models.DateField()
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    total = models.FloatField(default=0.0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("area", "fecha", "hora_inicio", "hora_fin")  
        # Evita que se duplique la misma reserva en un mismo horario

    def __str__(self):
        return f"Reserva {self.area.nombre} por {self.persona.nombres} el {self.fecha}"
