from rest_framework import serializers
from ChangApp.servicio.models import Servicio
from ChangApp.usuario.models.usuarioModels import Usuario

class BuscarUsuarioSerializer(serializers.Serializer):
    username = serializers.CharField(source='proveedor.username')
    first_name = serializers.CharField(source='proveedor.first_name')
    last_name = serializers.CharField(source='proveedor.last_name')
    fotoPerfil = serializers.ImageField(source='proveedor.fotoPerfil')
    servicios = serializers.SerializerMethodField()

    def get_servicios(self, obj):
        servicios = Servicio.objects.filter(proveedores_servicio__proveedor=obj.proveedor).distinct()

        resultado = []
        for servicio in servicios:
            resultado.append({
                "id": servicio.id,
                "nombreServicio": servicio.nombreServicio,
                "descripcion": servicio.descripcion,
                "dias": [
                    {
                        "dia": dia.dia,
                        "desdeHora": dia.desdeHora,
                        "hastaHora": dia.hastaHora
                    } for dia in servicio.dias.all()
                ]
            })

        return resultado
