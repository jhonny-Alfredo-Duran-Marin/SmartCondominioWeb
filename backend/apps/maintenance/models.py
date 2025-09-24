
from django.db import models
from django.core.exceptions import ValidationError
from apps.accounts.models import Persona, Personal
from django.conf import settings

User = settings.AUTH_USER_MODEL

#-------------------------------
# Modelos para la gestión de condominios
#-------------------------------
class Condominio(models.Model):
    ciudad = models.CharField(max_length=100)
    direccion = models.CharField(max_length=150)
    nit = models.CharField(max_length=30, unique=True)
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f"{self.nombre} - {self.ciudad}"

#-------------------------------
# Modelos para la gestión de bloques, unidades y activos
#-------------------------------
class Bloque(models.Model):
    descripcion = models.TextField(blank=True)
    nombre = models.CharField(max_length=50)
    condominio = models.ForeignKey(Condominio, on_delete=models.CASCADE, related_name="bloques")

    class Meta:
        unique_together = ("nombre", "condominio")  # No repetir nombre de bloque en el mismo condominio

    def __str__(self):
        return f"Bloque {self.nombre} ({self.condominio.nombre})"

#-------------------------------
# Modelos para la gestión de unidades y activos
#-------------------------------
class Unidad(models.Model):
    class Estado(models.TextChoices):
        DISPONIBLE = "Disponible", "Disponible"
        OCUPADO = "Ocupado", "Ocupado"

    area = models.FloatField()
    codigo = models.CharField(max_length=20)
    estado = models.CharField(max_length=20, choices=Estado.choices, default=Estado.DISPONIBLE)
    mantenimiento = models.FloatField(default=0.0)
    numero = models.IntegerField()
    piso = models.CharField(max_length=20)
    bloque = models.ForeignKey(Bloque, on_delete=models.CASCADE, related_name="unidades")

    class Meta:
        unique_together = ("codigo", "bloque")  # Evita duplicar códigos en el mismo bloque

    def clean(self):
        if self.area <= 0:
            raise ValidationError("El área debe ser mayor a 0")
        if self.mantenimiento < 0:
            raise ValidationError("El costo de mantenimiento no puede ser negativo")

    def __str__(self):
        return f"Unidad {self.codigo} ({self.estado})"

#-------------------------------
# Modelos para la gestión de activos
#-------------------------------
class Activo(models.Model):
    class Estado(models.TextChoices):
        ACTIVO = "Activo", "Activo"
        INACTIVO = "Inactivo", "Inactivo"

    categoria = models.CharField(max_length=50)
    estado = models.CharField(max_length=20, choices=Estado.choices, default=Estado.ACTIVO)
    nombre = models.CharField(max_length=100)
    ubicacion = models.CharField(max_length=100)
    condominio = models.ForeignKey(Condominio, on_delete=models.CASCADE, related_name="activos")

    class Meta:
        unique_together = ("nombre", "condominio")  # Un activo no se repite dentro del mismo condominio

    def clean(self):
        if not self.nombre.strip():
            raise ValidationError("El nombre del activo no puede estar vacío")

    def __str__(self):
        return f"{self.nombre} ({self.estado})"

#-------------------------------
# Modelos para la gestión de órdenes de trabajo y tareas
#-------------------------------

class OrdenTrabajo(models.Model):
    class Estado(models.TextChoices):
        SOLICITADO = "Solicitado", "Solicitado"
        PENDIENTE = "Pendiente", "Pendiente"
        ASIGNADO = "Asignado", "Asignado"
        EN_PROCESO = "EnProceso", "En Proceso"
        COMPLETO = "Completo", "Completo"

    class Prioridad(models.TextChoices):
        ALTA = "Alta", "Alta"
        MEDIA = "Media", "Media"
        BAJA = "Baja", "Baja"

    class Tipo(models.TextChoices):
        PREVENTIVO = "Preventivo", "Preventivo"
        CORRECTIVO = "Correctivo", "Correctivo"

    activo = models.ForeignKey(Activo, on_delete=models.CASCADE, related_name="ordenes")
    solicitante = models.ForeignKey(Persona, on_delete=models.SET_NULL, null=True, blank=True, related_name="solicitudes")
    titulo = models.CharField(max_length=150)
    descripcion = models.TextField()
    costo_estimado = models.FloatField(default=0.0)
    costo_real = models.FloatField(default=0.0)
    estado = models.CharField(max_length=20, choices=Estado.choices, default=Estado.SOLICITADO)
    prioridad = models.CharField(max_length=10, choices=Prioridad.choices, default=Prioridad.MEDIA)
    tipo = models.CharField(max_length=15, choices=Tipo.choices, default=Tipo.CORRECTIVO)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.titulo} ({self.estado})"

#-------------------------------
# Modelos para la gestión de tareas dentro de órdenes de trabajo
#-------------------------------
class Tarea(models.Model):
    class Estado(models.TextChoices):
        INICIO = "Inicio", "Inicio"
        EN_PROCESO = "EnProceso", "En Proceso"
        COMPLETO = "Completo", "Completo"

    orden = models.ForeignKey(OrdenTrabajo, on_delete=models.CASCADE, related_name="tareas")
    asignado_a = models.ForeignKey(Personal, on_delete=models.SET_NULL, null=True, blank=True, related_name="tareas")
    descripcion = models.TextField()
    estado = models.CharField(max_length=20, choices=Estado.choices, default=Estado.INICIO)
    fecha_programada = models.DateField(null=True, blank=True)
    fecha_ejecucion = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Tarea {self.id} - {self.estado}"

#-------------------------------
# Modelo para el seguimiento de cambios en las tareas
#-------------------------------
class SeguimientoTarea(models.Model):
    tarea = models.ForeignKey("Tarea", on_delete=models.CASCADE, related_name="seguimientos")
    descripcion = models.TextField()
    estado_anterior = models.CharField(max_length=20, blank=True, null=True)
    estado_nuevo = models.CharField(max_length=20)
    fecha = models.DateTimeField(auto_now_add=True)
    actualizado_por = models.ForeignKey("accounts.Personal", on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Seguimiento Tarea {self.tarea_id}: {self.estado_anterior} → {self.estado_nuevo}"


