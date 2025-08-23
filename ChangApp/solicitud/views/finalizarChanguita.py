from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from ChangApp.notificacion.models import Notificacion
from ChangApp.solicitud.models import EstadoServicio, Solicitud
from django.core.mail import send_mail
from django.conf import settings
from ChangApp.usuario.models.usuarioModels import Usuario

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

            if solicitud.cliente != request.user:
                return Response({"error": "No sos el cliente asignado."}, status=403)

            solicitud.estado = EstadoServicio.FINALIZADO
            solicitud.fechaTrabajo = timezone.now()
            solicitud.save()

            mensaje = (
                f"👋 Hola {solicitud.proveedorServicio.proveedor.first_name} {solicitud.proveedorServicio.proveedor.last_name}!\n\n"
                f"Te informamos que {solicitud.cliente.first_name} {solicitud.cliente.last_name} ha marcado como finalizada la changuita que tenías en curso. ✅\n\n"
                f"Podés ingresar a la app para ver los detalles del trabajo. ⭐\n\n"
                f"Gracias por brindar tus servicios a través de ChangApp.\n\n"
                f"Saludos,\n"
                f"El equipo de ChangApp"
                )
            Notificacion.objects.create(
                usuario_destino=solicitud.proveedorServicio.proveedor,
                notificacion_de_sistema=False,
                mensaje=mensaje
            )
            usuario_proveedor = solicitud.proveedorServicio.proveedor.email
            email_destino = usuario_proveedor

               
            # Enviar email al proveedor
            if email_destino:
                send_mail(
                    subject='Changuita finalizada',
                    message=mensaje,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[email_destino],
                    fail_silently=False,
                )

            return Response({
                "success": "Changuita finalizada.",
                "email_enviado_a": email_destino
            }, status=200)

        except Solicitud.DoesNotExist:
            return Response({"error": "Solicitud no encontrada."}, status=404)
