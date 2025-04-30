from rest_framework import serializers
from ChangApp.notificacion.models import Notificacion

class NotificacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notificacion
        fields = ['id', 'fechahora_creada', 'mensaje', 'tipo_sistema', 'usuario_destino']