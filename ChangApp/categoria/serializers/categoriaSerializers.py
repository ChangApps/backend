from rest_framework import serializers
from ChangApp.categoria.models import Categoria
from ChangApp.servicio.models.servicioModels import  Servicio

class CategoriaSerializer(serializers.ModelSerializer):
    categoria_padre = serializers.PrimaryKeyRelatedField(queryset=Categoria.objects.all(), allow_null=True)
    servicio = serializers.PrimaryKeyRelatedField(queryset=Servicio.objects.all())
    class Meta:
        model = Categoria
        fields = ['id', 'nombre', 'categoria_padre', 'servicio']