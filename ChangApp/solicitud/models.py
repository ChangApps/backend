from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from ChangApp.usuario.models.usuarioModels import Usuario
from ChangApp.notificacion.models import Notificacion
from ChangApp.servicio.models.proveedorServicioModels import ProveedorServicio

class EstadoServicio(models.TextChoices):
    INICIADO = 'I', 'Iniciado'
    FINALIZADO = 'F', 'Finalizado'
    CANCELADO = 'C', 'Cancelado'

class Solicitud (models.Model):
    comentario = models.TextField(null=True)
    fechaSolicitud = models.DateField(blank=True, null=True)
    fechaTrabajo = models.DateField(blank=True, null=True)
    fechaValoracion = models.DateField(blank=True, null=True)
    valoracion = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], null=True, blank=True)
    proveedorServicio = models.ForeignKey(ProveedorServicio, on_delete=models.CASCADE, related_name='solicitudes')
    cliente = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='solicitudes_cliente')
    notificacion = models.ForeignKey(Notificacion, on_delete=models.CASCADE, null=True, blank=True, related_name='solicitudes_notificacion')
    estado = models.CharField(max_length=15, choices=EstadoServicio.choices, default=EstadoServicio.INICIADO)

    def __str__(self) -> str:
        return f"Cliente: {self.cliente.get_username()},  Proveedor: {self.proveedorServicio.proveedor.get_username()}"

    def save(self) :
        a= super().save()
        self.cliente.calcularCantServiciosContratados()
        self.proveedorServicio.proveedor.calcularCantServiciosTrabajados()
        self.proveedorServicio.proveedor.calcularPuntaje()
        return a
    
    def delete(self, *args, **kwargs):
        # Elimino y después actualizo valores
        super().delete(*args, **kwargs)
        self.cliente.calcularCantServiciosContratados()
        self.proveedorServicio.proveedor.calcularCantServiciosTrabajados()
        self.proveedorServicio.proveedor.calcularPuntaje()