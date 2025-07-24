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

            comentario_texto = f"✍️ Comentario: \"{comentario}\"\n\n" if comentario else ""

            mensaje = (
                f"Hola {solicitud.proveedorServicio.proveedor.first_name},\n\n"
                f"{solicitud.cliente.first_name} acaba de dejar una valoración sobre la changuita que realizaste. ⭐\n\n"
                f"{comentario_texto}"
                f"📱 Podés revisar la valoración completa ingresando a la app.\n\n"
                f"Gracias por ofrecer tus servicios en ChangApp 💙\n\n"
                f"Saludos,\n"
                f"El equipo de Changuitas"
            )
            
            proveedor = solicitud.proveedorServicio.proveedor
            email_destino = proveedor.email

            # Notificación
            Notificacion.objects.create(
                usuario_destino=proveedor,
                notificacion_de_sistema=False,
                mensaje=mensaje
            )

            # Enviar email al proveedor
            if email_destino:
                send_mail(
                    subject='¡Recibiste una nueva valoración!',
                    message=mensaje,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[email_destino],
                    fail_silently=False,
                )

            return Response({
                "success": "Valoración registrada.",
                "email_enviado_a": email_destino
            }, status=200)

        except Solicitud.DoesNotExist:
            return Response({"error": "Solicitud no encontrada."}, status=404)