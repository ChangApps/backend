from django.db import models

# Enumeración para los días de la semana, útil para evitar errores tipográficos y mantener consistencia
class DiasSemana(models.TextChoices):
    LUNES = "Lunes", "Lun"
    MARTES = "Martes", "Mar"
    MIERCOLES = "Miércoles", "Mie"
    JUEVES = "Jueves", "Jue"
    VIERNES = "Viernes", "Vie"
    SABADO = "Sábado", "Sab"
    DOMINGO = "Domingo", "Dom"

# Modelo principal que representa un tipo de servicio que puede ofrecer un proveedor
class Servicio(models.Model):
    # Nombre del servicio, obligatorio
    nombreServicio = models.CharField(max_length=100, null=False)

    # Relación ManyToMany con Categoría (se asume que 'categoria.Categoria' está definido en otra app)
    categorias = models.ManyToManyField('categoria.Categoria', related_name='servicios')

    # Descripción del servicio, también obligatoria
    descripcion = models.TextField(null=False)

    # Método auxiliar para obtener los proveedores asociados al servicio
    def obtener_proveedores(self):
        # Accede a la relación inversa con el modelo intermedio ProveedorServicio (no incluido aquí)
        proveedores_servicio = self.proveedores_servicio.all()

        # Retorna la lista de proveedores desde la relación intermedia
        proveedores = [ps.proveedor for ps in proveedores_servicio]
        return proveedores

    # Representación del servicio como string
    def __str__(self) -> str:
        return self.nombreServicio

# Modelo que representa los días y horarios en los que se ofrece un servicio
class HorarioServicio(models.Model):
    # Relación con el servicio al que pertenece este horario
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE, related_name='dias')

    # Día de la semana (seleccionado desde el enum DiasSemana)
    dia = models.CharField(max_length=10, choices=DiasSemana.choices, null=False)

    # Hora de inicio del servicio
    desdeHora = models.TimeField(null=False)

    # Hora de finalización del servicio
    hastaHora = models.TimeField(null=False)

    # Representación del horario como string
    def __str__(self):
        return f"{self.servicio.nombreServicio} - {self.dia} {self.desdeHora} a {self.hastaHora}"
