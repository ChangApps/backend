from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from ChangApp.notificacion.models import Notificacion
from ChangApp.notificacion.serializers import notificacionSerializer
from drf_yasg.utils import swagger_auto_schema

class NotificacionesPorUsuarioView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(operation_description="Devuelve las notificaciones del usuario autenticado")
    def get(self, request):
        notificaciones = Notificacion.objects.filter(usuario_destino=request.user).order_by('-fechahora_creada')
        serializer = notificacionSerializer(notificaciones, many=True)
        return Response(serializer.data)
