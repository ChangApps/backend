from django.db import models

class Notificacion(models.Model):
    fechahora_creada = models.DateTimeField(null=True)
    mensaje = models.TextField(null=True)
    tipo_sistema = models.BooleanField()
    usuario_destino = models.ForeignKey('usuario.Usuario', on_delete=models.CASCADE, blank=True, null=True, related_name='notificaciones')

    def __str__(self):
        return f"Notificación para {self.usuario.username}: {self.mensaje[:20]}"