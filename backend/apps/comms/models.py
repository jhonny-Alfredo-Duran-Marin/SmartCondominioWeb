from django.db import models
from django.conf import settings  # Esto apunta al AUTH_USER_MODEL (User)

User = settings.AUTH_USER_MODEL

#-------------------------------
# Modelos para la gestión de avisos y notificaciones
#-------------------------------
class Aviso(models.Model):
    class Tipo(models.TextChoices):
        GENERAL = "General", "General"
        RESIDENTE = "Residente", "Residente"
        SEGURIDAD = "Seguridad", "Seguridad"
        MANTENIMIENTO = "Mantenimiento", "Mantenimiento"

    titulo = models.CharField(max_length=150)
    cuerpo = models.TextField()
    adjunto_url = models.CharField(max_length=250, blank=True, null=True)
    tipo = models.CharField(max_length=20, choices=Tipo.choices, default=Tipo.GENERAL)
    publicado_en = models.DateTimeField(auto_now_add=True)

    # 👇 Relación con el usuario que publica
    publicado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="avisos_publicados"
    )

    def __str__(self):
        return self.titulo

#-------------------------------
# Modelos para la gestión de tokens de notificaciones push
#-------------------------------
class PushToken(models.Model):
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="tokens"
    )
    token = models.CharField(max_length=250, unique=True)
    plataforma = models.CharField(max_length=20)  # Android, iOS, Web
    last_seen_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.usuario} - {self.plataforma}"

#-------------------------------
# Modelos para la gestión de destinatarios de avisos
#-------------------------------
class AvisoDestinatario(models.Model):
    aviso = models.ForeignKey(Aviso, on_delete=models.CASCADE, related_name="destinatarios")
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="avisos_recibidos")
    leido_en = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.usuario} - {self.aviso.titulo}"

