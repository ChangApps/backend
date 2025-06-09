from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from ChangApp.notificacion.models import Notificacion
from ChangApp.solicitud.models import EstadoServicio, Solicitud
from django.core.mail import send_mail
from django.conf import settings

class CancelarChanguitaView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="El cliente o el proveedor cancela la changuita",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['solicitud_id'],
            properties={
                'solicitud_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID de la solicitud a cancelar'),
            },
        ),
        responses={200: 'Changuita cancelada correctamente'}
    )
    def post(self, request):
        solicitud_id = request.data.get("solicitud_id")

        try:
            solicitud = Solicitud.objects.get(id=solicitud_id)
            usuario_actual = request.user

            # Verificar si el usuario es cliente o proveedor
            if solicitud.cliente == usuario_actual:
                mensaje = f"{usuario_actual.username} ha cancelado la changuita."
                destino = solicitud.proveedorServicio.proveedor if solicitud.proveedorServicio else None
            elif solicitud.proveedorServicio and solicitud.proveedorServicio.proveedor == usuario_actual:
                mensaje = f"{usuario_actual.username} ha cancelado la changuita."
                destino = solicitud.cliente
            else:
                return Response({"error": "No estás autorizado para cancelar esta changuita."}, status=403)

            # Cambiar estado sin eliminar el proveedorServicio
            solicitud.estado = EstadoServicio.CANCELADO
            solicitud.save()

            email_destino = None

            # Crear notificación, aunque destino sea None
            Notificacion.objects.create(
                usuario_destino=destino,
                notificacion_de_sistema=False,
                mensaje=mensaje
            )

            # Enviar email si hay destino y tiene email
            if destino and destino.email:
                email_destino = destino.email
                send_mail(
                    subject='Changuita Cancelada',
                    message=mensaje,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[email_destino],
                    fail_silently=False,
                )

            return Response({
                "success": "Changuita cancelada correctamente.",
                "email_enviado_a": email_destino
            }, status=200)

        except Solicitud.DoesNotExist:
            return Response({"error": "Solicitud no encontrada."}, status=404)