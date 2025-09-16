from django.db import models
from django.db.models import Q, F 
from django.conf import settings
# Create your models here.
#-------------CLASE PERSONA----------------
# Esta clase representa a una persona en el sistema.
# Contiene información personal y de contacto.
# Está vinculada a un usuario del sistema mediante una relación uno a uno.
#-------------------------------------------
class Persona(models.Model):
    class Estado(models.TextChoices):
        ACTIVO = 'Activo', 'Activo'
        INACTIVO = 'Inactivo', 'Inactivo'
        SUSPENDIDO = 'Suspendido', 'Suspendido'

    class Tipo(models.TextChoices):
         PADRE = "Padre", "Padre"
         MADRE = "Madre", "Madre"
         HIJO = "Hijo", "Hijo",
         CONYUGE = "Conyuge", "Conyuge"
         OTRO = "Otro", "Otro"

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='persona'
    )
    ci=models.CharField("CI", max_length=20, unique=True)
    nombres=models.CharField(max_length=50)
    apellidos=models.CharField(max_length=50)
    telefono=models.CharField(max_length=30, blank=True)
    fecha_nacimiento=models.DateField(null=True, blank=True)
    estado = models.CharField(max_length=10, choices=Estado.choices, default=Estado.ACTIVO)
    tipo = models.CharField(max_length=10, choices=Tipo)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # clave: relación recursiva
    jefe = models.ForeignKey(
        'self',
        null=True, blank=True,
        related_name='dependientes',
        on_delete=models.PROTECT
    )
    # Restricción para evitar que alguien sea su propio jefe
    class Meta:
        constraints = [
            # Evita que alguien sea su propio jefe
            models.CheckConstraint(check=~Q(id=F('jefe')), name='persona_no_es_su_propio_jefe'),
        ]

    def familia(self):
        """Devuelve el conjunto de miembros de su familia (incluyéndose al jefe)."""
        head = self if self.es_jefe() else self.jefe
        # todos los que apuntan al jefe + el jefe
        return Persona.objects.filter(Q(id=head.id) | Q(jefe=head))
    
    def es_jefe(self):
        return self.jefe_id is None
    
    def __str__(self):
        return f"{self.apellidos} {self.nombres} ({self.ci})"

#-------------CLASE PERSONAL----------------
# Esta clase representa al personal del sistema.
# Contiene información específica del personal de trabajo.
# Está vinculada a una usuario mediante una relación uno a uno.
#-------------------------------------------
class Personal(models.Model):
    class Estado(models.TextChoices):
        ACTIVO = 'Activo', 'Activo'
        INACTIVO = 'Inactivo', 'Inactivo'
        SUSPENDIDO = 'Suspendido', 'Suspendido'

    class Tipo(models.TextChoices):
         LIMPIEZA = "Limpieza", "Limpieza"
         SEGURIDAD = "Seguridad", "Seguridad"
         MANTENIMIENTO = "Mantenimiento", "Mantenimiento"
    
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete= models.CASCADE,
        related_name = "personal"
    )
    nombre = models.CharField(max_length=50)
    apellidos= models.CharField(max_length = 50)
    cargo = models.CharField(max_length = 30)
    estado = models.CharField(max_length=10, choices=Estado.choices, default=Estado.ACTIVO)
    sueldo = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    fecha_contratacion = models.DateField()
    tipo = models.CharField(max_length = 20, choices=Tipo.choices)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.apellidos} - {self.nombre} , {self.cargo}"
