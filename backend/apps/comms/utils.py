from .models import Aviso, AvisoDestinatario, PushToken

def enviar_notificacion_push(usuario, titulo, cuerpo):
    # Guardar en la BD como aviso
    aviso = Aviso.objects.create(
        titulo=titulo,
        cuerpo=cuerpo,
        publicado_por=usuario
    )
    AvisoDestinatario.objects.create(aviso=aviso, usuario=usuario)

    # Buscar tokens
    tokens = PushToken.objects.filter(usuario=usuario)
    for t in tokens:
        print(f"📲 Enviar push a {t.plataforma} - Token {t.token}: {titulo} - {cuerpo}")
        # Aquí en producción conectas con Firebase / Expo / OneSignal
