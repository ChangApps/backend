from django.db import models
from ChangApp.usuario.models.usuarioModels import Usuario
from ChangApp.servicio.models.servicioModels import Servicio

class ProveedorServicio(models.Model):
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE, related_name='proveedores_servicio')
    proveedor = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='servicios_ofrecidos')
    fechaDesde = models.DateField()
    fechaHasta = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"Servicio: {self.servicio.nombreServicio}, Proveedor: {self.proveedor.get_username()}"