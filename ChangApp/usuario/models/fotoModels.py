from django.db import models
from ChangApp.usuario.models.usuarioModels import Usuario

class Fotos(models.Model):
    fotos = models.ImageField(upload_to='imagenesProveedor')
    fechaHora = models.DateTimeField(blank=True, null=False)
    proveedor = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='fotos')