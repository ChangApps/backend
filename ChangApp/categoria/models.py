from django.db import models
from ChangApp.servicio.models.servicioModels import Servicio

class Categoria (models.Model):
    nombre = models.CharField(max_length=100, null=True)
    categoria_padre = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='subcategorias')
    
    def __str__(self) -> str:
        return self.nombre
