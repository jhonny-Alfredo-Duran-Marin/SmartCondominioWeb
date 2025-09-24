from django.db import models
from apps.accounts.models import Persona
from apps.maintenance.models import Unidad

#------------------------------
# Modelos de Propiedades y Ocupaciones
#------------------------------
class Propiedad(models.Model):
    TIPOS = [("Casa", "Casa"), ("Departamento", "Departamento")]

    persona = models.ForeignKey(
        Persona,
        on_delete=models.CASCADE,
        related_name="propiedades"
    )  # Dueño
    unidad = models.ForeignKey(
        Unidad,
        on_delete=models.CASCADE,
        related_name="propiedades"
    )
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField(null=True, blank=True)
    tipo = models.CharField(max_length=20, choices=TIPOS)
    porcentaje = models.FloatField(help_text="Porcentaje de copropiedad")

    def __str__(self):
        return f"{self.persona} es dueño de {self.unidad}"

#------------------------------
# Modelo de Ocupaciones
#------------------------------
class Ocupacion(models.Model):
    ROLES = [
        ("Titular", "Titular"),
        ("Conyuge", "Cónyuge"),
        ("Hijo", "Hijo"),
        ("Inquilino", "Inquilino"),
    ]
    ESTADOS = [("Activo", "Activo"), ("Inactivo", "Inactivo")]

    persona = models.ForeignKey(
        Persona,
        on_delete=models.CASCADE,
        related_name="ocupaciones"
    )
    unidad = models.ForeignKey(
        Unidad,
        on_delete=models.CASCADE,
        related_name="ocupantes"
    )
    rol_hogar = models.CharField(max_length=20, choices=ROLES)
    estado = models.CharField(max_length=10, choices=ESTADOS, default="Activo")
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.persona} ({self.rol_hogar}) en {self.unidad}"
