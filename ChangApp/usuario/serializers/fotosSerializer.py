from rest_framework import serializers
from ChangApp.usuario.models.fotoModels import Fotos

class FotosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fotos
        fields = ['id', 'fotos', 'fechaHora', 'proveedor']