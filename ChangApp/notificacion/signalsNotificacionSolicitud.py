from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Notificacion
from proyecto.utils.firebase_utils import enviar_notificacion_push

@receiver(post_save, sender=Notificacion)
def enviar_push_al_crear_notificacion(sender, instance, created, **kwargs):
    if created and not instance.notificacion_de_sistema:
        usuario = instance.usuario_destino
        if usuario.fcm_token:
            try:
                enviar_notificacion_push(
                    token=usuario.fcm_token,
                    titulo="Notificación de ChangApp",
                    cuerpo=instance.mensaje
                )
            except Exception as e:
                print("Error al enviar push desde signal:", e)
