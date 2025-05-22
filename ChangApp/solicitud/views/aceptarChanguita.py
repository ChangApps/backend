from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from ChangApp.notificacion.models import Notificacion
from ChangApp.solicitud.models import EstadoServicio, Solicitud

class AceptarChanguitaView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="El proveedor acepta la changuita",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['solicitud_id'],
            properties={
                'solicitud_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID de la solicitud a aceptar'),
            },
        ),
        responses={200: 'Changuita aceptada'}
    )

    def post(self, request):
        solicitud_id = request.data.get("solicitud_id")

        try:
            solicitud = Solicitud.objects.get(id=solicitud_id)

            # Validar que el proveedor actual sea el que fue asignado
            if solicitud.proveedorServicio.proveedor != request.user:
                return Response({"error": "No sos el proveedor asignado."}, status=403)

            # Cambiar estado a iniciado
            solicitud.estado = EstadoServicio.INICIADO
            solicitud.save()

            mensaje = f"{request.user.username} aceptó tu solicitud de changuita. Ponte en contacto para coordinar con él/ella!"
            Notificacion.objects.create(
                usuario_destino=solicitud.cliente,
                notificacion_de_sistema=False,
                mensaje=mensaje
            )

            return Response({"success": "Changuita aceptada y comenzada."}, status=200)

        except Solicitud.DoesNotExist:
            return Response({"error": "Solicitud no encontrada."}, status=404)
