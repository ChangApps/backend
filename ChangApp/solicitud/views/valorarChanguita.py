from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from ChangApp.notificacion.models import Notificacion
from ChangApp.solicitud.models import EstadoServicio, Solicitud

class ValorarChanguitaView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="El cliente valora la changuita (1 a 5) y deja un comentario",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['solicitud_id', 'valoracion'],
            properties={
                'solicitud_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID de la solicitud a valorar'),
                'valoracion': openapi.Schema(type=openapi.TYPE_INTEGER, description='Valoración del 1 al 5'),
                'comentario': openapi.Schema(type=openapi.TYPE_STRING, description='Comentario opcional'),
            },
        ),
        responses={200: 'Valoración registrada'}
    )

    def post(self, request):
        solicitud_id = request.data.get("solicitud_id")
        valoracion = request.data.get("valoracion")
        comentario = request.data.get("comentario")

        try:
            solicitud = Solicitud.objects.get(id=solicitud_id)

            if solicitud.cliente != request.user:
                return Response({"error": "No sos el cliente de esta changuita."}, status=403)

            if solicitud.estado != EstadoServicio.FINALIZADO:
                return Response({"error": "Solo podés valorar changuitas finalizadas."}, status=400)

            solicitud.valoracion = valoracion
            solicitud.comentario = comentario
            solicitud.fechaValoracion = timezone.now()
            solicitud.save()

            mensaje = f"{request.user.username} ha dejado un comentario sobre tu trabajo realizado."
            Notificacion.objects.create(
                usuario_destino=solicitud.proveedorServicio.proveedor,
                notificacion_de_sistema=False,
                mensaje=mensaje
            )

            return Response({"success": "Valoración registrada."}, status=200)

        except Solicitud.DoesNotExist:
            return Response({"error": "Solicitud no encontrada."}, status=404)
