from rest_framework import serializers
from ChangApp.notificacion.models import Notificacion

class NotificacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notificacion
        fields = ['id', 'fechaHora', 'mensaje', 'tipoSistema', 'Usuario']