from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class EstadoServicio(models.TextChoices):
    PENDIENTE_ACEPTACION = 'PA', 'Pendiente de Aceptación'
    INICIADO = 'I', 'Iniciado'
    FINALIZADO = 'F', 'Finalizado'
    CANCELADO = 'C', 'Cancelado'

class Solicitud(models.Model):
    fechaSolicitud = models.DateField(blank=True, null=True, auto_now_add=True)
    fechaTrabajo = models.DateField(blank=True, null=True)
    fechaValoracion = models.DateField(blank=True, null=True)
    valoracion = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], null=True, blank=True)
    comentario = models.TextField(null=True)
    proveedorServicio = models.ForeignKey('servicio.ProveedorServicio', on_delete=models.CASCADE, related_name='solicitudes')
    cliente = models.ForeignKey('usuario.Usuario', on_delete=models.CASCADE, related_name='solicitudes_cliente')
    estado = models.CharField(max_length=25, choices=EstadoServicio.choices, default=EstadoServicio.PENDIENTE_ACEPTACION)

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