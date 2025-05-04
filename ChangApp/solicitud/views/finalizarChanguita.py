from datetime import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from ChangApp.notificacion.models import Notificacion
from ChangApp.solicitud.models import EstadoServicio, Solicitud

class FinalizarChanguitaView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="El proveedor marca la changuita como finalizada",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['solicitud_id'],
            properties={
                'solicitud_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID de la solicitud a finalizar'),
            },
        ),
        responses={200: 'Changuita finalizada'}
    )

    def post(self, request):
        solicitud_id = request.data.get("solicitud_id")

        try:
            solicitud = Solicitud.objects.get(id=solicitud_id)

            if solicitud.proveedorServicio.proveedor != request.user:
                return Response({"error": "No sos el proveedor asignado."}, status=403)

            solicitud.estado = EstadoServicio.FINALIZADO
            solicitud.fechaTrabajo = timezone.now()
            solicitud.save()

            mensaje = f"{request.user.username} ha finalizado la changuita. Puntua su trabajo y dejale un comentario!."
            Notificacion.objects.create(
                usuario_destino=solicitud.cliente,
                notificacion_de_sistema=False,
                mensaje=mensaje
            )

            return Response({"success": "Changuita finalizada."}, status=200)

        except Solicitud.DoesNotExist:
            return Response({"error": "Solicitud no encontrada."}, status=404)
