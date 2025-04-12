from django.db import models

class DiasSemana(models.TextChoices):
    LUNES = "Lunes", "Lun"
    MARTES = "Martes", "Mar"
    MIERCOLES = "Miércoles", "Mie"
    JUEVES = "Jueves", "Jue"
    VIERNES = "Viernes", "Vie"
    SABADO = "Sábado", "Sab"
    DOMINGO = "Domingo", "Dom"
    
class Servicio(models.Model):
    nombreServicio = models.CharField(max_length=100, null=False)
    categorias = models.ManyToManyField('Categoria', related_name='servicios') #actualizar cardinalidad diagrama entidad relación
    descripcion = models.TextField(null=False)
    dia = models.CharField(max_length=10, choices=DiasSemana.choices,null=False, default="Lunes")
    desdeHora = models.TimeField(null=False, default="00:00")
    hastaHora = models.TimeField(null=False, default="00:00")

    def obtener_proveedores(self):
       # Retorna los usuarios que ofrecen este servicio.
        proveedores_servicio = self.proveedores_servicio.all()  # conexión con ProveedorServicio mediante related_name
        proveedores = [proveedor_servicio.proveedor for proveedor_servicio in proveedores_servicio]
        return proveedores

    def __str__(self) -> str:
        return self.nombreServicio
