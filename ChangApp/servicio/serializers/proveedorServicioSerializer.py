from rest_framework import serializers
from ChangApp.servicio.models.servicioModels import Servicio
from ChangApp.servicio.models.proveedorServicioModels import  ProveedorServicio
from ChangApp.usuario.models.usuarioModels import Usuario

class ProveedorServicioSerializer(serializers.ModelSerializer):
    servicio = serializers.PrimaryKeyRelatedField(queryset=Servicio.objects.all())
    proveedor = serializers.PrimaryKeyRelatedField(queryset=Usuario.objects.all())
    class Meta:
        model = ProveedorServicio
        fields = ['id', 'servicio', 'proveedor', 'fechaDesde', 'fechaHasta']