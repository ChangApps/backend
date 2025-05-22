from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from ChangApp.notificacion.models import Notificacion
from ChangApp.solicitud.models import EstadoServicio, Solicitud

class CancelarChanguitaView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="El proveedor cancela o rechaza la changuita",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['solicitud_id'],
            properties={
                'solicitud_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID de la solicitud a cancelar'),
            },
        ),
        responses={200: 'Changuita cancelada'}
    )

    def post(self, request):
        solicitud_id = request.data.get("solicitud_id")

        try:
            solicitud = Solicitud.objects.get(id=solicitud_id)

            if solicitud.proveedorServicio.proveedor != request.user:
                return Response({"error": "No sos el proveedor asignado."}, status=403)

            # Rechaza: elimina proveedor y vuelve al estado inicial
            solicitud.proveedorServicio = None
            solicitud.estado = EstadoServicio.CANCELADO  # Cancelado o volvés a un estado anterior
            solicitud.save()

            mensaje = f"{request.user.username} ha cancelado o rechazado tu solicitud de changuita. Si deseas, busca otro proveedor."
            Notificacion.objects.create(
                usuario_destino=solicitud.cliente,
                notificacion_de_sistema=False,
                mensaje=mensaje
            )

            return Response({"success": "Changuita rechazada."}, status=200)

        except Solicitud.DoesNotExist:
            return Response({"error": "Solicitud no encontrada."}, status=404)
