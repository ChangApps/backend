from django.db import models

class Direccion(models.Model):
    calle = models.CharField(max_length=100, null=False)
    altura = models.IntegerField(null=False)
    nroDepto = models.IntegerField(blank=True, null=True)
    piso = models.IntegerField(blank=True, null=True)
    barrio = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.calle}, {self.altura}"