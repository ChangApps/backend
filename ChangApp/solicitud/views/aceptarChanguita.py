from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from ChangApp.notificacion.models import Notificacion
from ChangApp.solicitud.models import EstadoServicio, Solicitud
from django.core.mail import send_mail
from django.conf import settings
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

            mensaje = (
                f"🎉 Buenas noticias, {solicitud.cliente.first_name} {solicitud.cliente.last_name}!\n\n"
                f"{request.user.first_name} {request.user.last_name} aceptó tu solicitud de changuita. 🙌\n\n"
                f"Ahora pueden ponerse en contacto para coordinar los detalles del servicio.\n\n"
                f"Gracias por usar Changuitas. Estamos felices de ayudarte a concretar tus tareas. \n\n"
                f"🔔 Recordá que podés ver el estado de esta changuita en la app.\n\n"
                f"Saludos,\n"
                f"El equipo de Changuitas"
            )
            destinatario_email = solicitud.cliente.email

            # Crear notificación
            Notificacion.objects.create(
                usuario_destino=solicitud.cliente,
                notificacion_de_sistema=False,
                mensaje=mensaje
            )

            # Enviar email
            if destinatario_email:
                send_mail(
                    subject='Solicitud de changuita aceptada',
                    message=mensaje,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[destinatario_email],
                    fail_silently=False,
                )

            return Response({
                "success": "Changuita aceptada y comenzada.",
                "email_enviado_a": destinatario_email
            }, status=200)

        except Solicitud.DoesNotExist:
            return Response({"error": "Solicitud no encontrada."}, status=404)