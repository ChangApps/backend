from rest_framework import serializers
from ChangApp.usuario.models.usuarioModels import  Usuario
from ChangApp.solicitud.models import Solicitud,EstadoServicio
from ChangApp.notificacion.models import Notificacion

class SolicitudSerializer(serializers.ModelSerializer):
    cliente = serializers.PrimaryKeyRelatedField(queryset=Usuario.objects.all())
    notificacion = serializers.PrimaryKeyRelatedField(queryset=Notificacion.objects.all(), required=False, allow_null=True)
    valoracion = serializers.IntegerField(allow_null=True, required=False)
    estado = serializers.ChoiceField(choices=EstadoServicio.choices)
    estado_display = serializers.SerializerMethodField()

    proveedor_id = serializers.SerializerMethodField()
    nombreServicio = serializers.SerializerMethodField()  
    cliente_nombre = serializers.SerializerMethodField() 

    servicio_id = serializers.SerializerMethodField()

    def get_servicio_id(self, obj):
        if obj.proveedorServicio and obj.proveedorServicio.servicio:
            return obj.proveedorServicio.servicio.id
        return None

    class Meta:
        model = Solicitud
        fields = [
            'id', 'comentario', 'fechaSolicitud', 'fechaTrabajo', 
            'fechaValoracion', 'valoracion', 'proveedorServicio', 
            'cliente', 'notificacion', 'estado', 'estado_display', 'proveedor_id','nombreServicio','cliente_nombre','servicio_id'
        ]

    def create(self, validated_data):
        # Nos aseguramos que el estado esté establecido correctamente
        estado = validated_data.get('estado', EstadoServicio.INICIADO)  # 'I' va a hacer el estado predeterminado
        validated_data['estado'] = estado  

        # Creamos y guardamos la instancia de solicitud
        solicitud = Solicitud(**validated_data)
        solicitud.save()  # Guardamos la solicitud normalmente
        return solicitud

    def get_estado_display(self, obj):
        return obj.get_estado_display()
    
    @staticmethod
    def obtener_historial(cliente_id):
        solicitudes = Solicitud.objects.filter(cliente=cliente_id)
        # serializer para las solicitudes
        serializer = SolicitudSerializer(solicitudes, many=True)
         # retornamos los datos serializados
        return serializer.data

#Necesitamos el proveedor id para obtener sus dato en el front,por eso se agrego que devuelve el atributo en la respuesta
    def get_proveedor_id(self, obj):
        return obj.proveedorServicio.proveedor.id if obj.proveedorServicio else None
    
    def get_nombreServicio(self, obj):
        # Obtenemos el nombre del servicio relacionado con la solicitud
        return obj.proveedorServicio.servicio.nombreServicio if obj.proveedorServicio else None
    
    def get_cliente_nombre(self, obj):
        # Concatenamos el nombre y apellido del cliente (utilizado en las resenias)
        return f"{obj.cliente.first_name} {obj.cliente.last_name}" if obj.cliente else None