from rest_framework import serializers
from ChangApp.servicio.models.servicioModels import Servicio

class ServicioSerializer(serializers.ModelSerializer):
    dias = serializers.SerializerMethodField()

    class Meta:
        model = Servicio
        fields = ['id', 'nombreServicio', 'descripcion', 'dia', 'desdeHora', 'hastaHora', 'dias']

    def get_dias(self, obj):
        # Si existen múltiples servicios con el mismo nombre, devuelva todos sus días/horas
        servicios = Servicio.objects.filter(nombreServicio=obj.nombreServicio)
        return [
            {
                'dia': servicio.dia,
                'desdeHora': servicio.desdeHora,
                'hastaHora': servicio.hastaHora
            } for servicio in servicios
        ]
    
    # Validación general para verificar que desdeHora sea menor que hastaHora
    def validate(self, data):
        if data['desdeHora'] >= data['hastaHora']:
            raise serializers.ValidationError("La hora de inicio debe ser menor que la hora de fin.")
        return data
