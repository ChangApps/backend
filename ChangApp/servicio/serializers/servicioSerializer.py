from ChangApp.servicio.models.proveedorServicioModels import ProveedorServicio
from rest_framework import serializers
from ChangApp.servicio.models.servicioModels import Servicio, HorarioServicio

# Serializador para el modelo HorarioServicio
class HorarioServicioSerializer(serializers.ModelSerializer):
    class Meta:
        model = HorarioServicio
        fields = ['dia', 'desdeHora', 'hastaHora']  # Campos que se expondrán en la API

    # Validación personalizada para asegurar que la hora de inicio sea menor que la de fin
    def validate(self, data):
        if data['desdeHora'] >= data['hastaHora']:
            raise serializers.ValidationError("La hora de inicio debe ser menor que la hora de fin.")
        return data

# Serializador para el modelo Servicio, que incluye los horarios (dias) como anidados
class ServicioSerializer(serializers.ModelSerializer):
    dias = HorarioServicioSerializer(many=True)  # Relación 1 a muchos: un servicio tiene varios horarios
    fechaDesde = serializers.SerializerMethodField() #Se agrega el campo fechaDesde para mostrar la fecha de inicio del servicio
    
    class Meta:
        model = Servicio
        fields = ['id', 'nombreServicio', 'descripcion', 'dias', 'fechaDesde']  # Campos del servicio + sus horarios

    # Método para crear un nuevo Servicio junto con sus horarios
    def create(self, validated_data):
        dias_data = validated_data.pop('dias')  # Se separan los datos de los horarios
        servicio = Servicio.objects.create(**validated_data)  # Se crea el Servicio
        for dia_data in dias_data:
            # Se crea cada HorarioServicio relacionado al servicio recién creado
            HorarioServicio.objects.create(servicio=servicio, **dia_data)
        return servicio
    
    def get_fechaDesde(self, servicio):
        proveedor = self.context.get('proveedor')
        if proveedor:
            relacion = ProveedorServicio.objects.filter(
                proveedor=proveedor, servicio=servicio
            ).order_by('-fechaDesde').first()
            if relacion:
                return relacion.fechaDesde
        return None

    # Método para actualizar un Servicio junto con sus horarios
    def update(self, instance, validated_data):
        dias_data = validated_data.pop('dias', None)  # Se separan los datos de los horarios (si vienen)
        
        # Se actualizan los campos del Servicio
        instance.nombreServicio = validated_data.get('nombreServicio', instance.nombreServicio)
        instance.descripcion = validated_data.get('descripcion', instance.descripcion)
        instance.save()

        # Si se envían horarios, se reemplazan completamente los existentes
        if dias_data is not None:
            instance.dias.all().delete()  # Se eliminan los horarios antiguos
            for dia_data in dias_data:
                HorarioServicio.objects.create(servicio=instance, **dia_data)  # Se crean los nuevos horarios
        
        return instance
