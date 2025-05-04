from django.db import models

class Notificacion(models.Model):
    fechahora_creada = models.DateTimeField(null=True, auto_now_add=True, editable=False)
    mensaje = models.TextField(null=True)
    notificacion_de_sistema = models.BooleanField() # Si es true es notificacion de sistema, sino es notificacion de evento
    usuario_destino = models.ForeignKey('usuario.Usuario', on_delete=models.CASCADE, blank=True, null=True, related_name='notificaciones')

    def __str__(self):
        return f"Notificación para {self.usuario_destino.username}: {self.mensaje[:50]}"