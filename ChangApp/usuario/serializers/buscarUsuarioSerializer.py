from rest_framework import serializers

class BuscarUsuarioSerializer(serializers.Serializer):
    id = serializers.IntegerField(source='proveedor.id')
    username = serializers.CharField(source='proveedor.username')
    first_name = serializers.CharField(source='proveedor.first_name')
    last_name = serializers.CharField(source='proveedor.last_name')
    fotoPerfil = serializers.ImageField(source='proveedor.fotoPerfil')
    servicios = serializers.SerializerMethodField()

    def get_servicios(self, obj):
        servicios = obj['servicios']  
        return [
            {
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
            }
            for servicio in servicios
        ]