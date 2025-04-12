from django.db import models
from ChangApp.usuario.models.usuarioModels import Usuario

class Notificacion(models.Model):
    fechaHora = models.DateTimeField(null=True)
    mensaje = models.TextField(null=True)
    tipoSistema = models.BooleanField()
    Usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='notificaciones')
