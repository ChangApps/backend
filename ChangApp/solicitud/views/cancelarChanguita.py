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
        motivo = request.data.get("motivo")

        try:
            solicitud = Solicitud.objects.get(id=solicitud_id)
            usuario_actual = request.user

            if solicitud.cliente == usuario_actual:
                destino = solicitud.proveedorServicio.proveedor if solicitud.proveedorServicio else None
            elif solicitud.proveedorServicio and solicitud.proveedorServicio.proveedor == usuario_actual:
                destino = solicitud.cliente
            else:
                return Response({"error": "No estás autorizado para cancelar esta changuita."}, status=403)

            # Cambiar estado
            solicitud.estado = EstadoServicio.CANCELADO
            solicitud.save()

            # Crear notificación
            Notificacion.objects.create(
                usuario_destino=destino,
                notificacion_de_sistema=False,
                mensaje=(
                    f"👋 Hola {destino.first_name} {destino.last_name},\n\n"
                    f"Lamentamos informarte que {usuario_actual.first_name} {usuario_actual.last_name} ha cancelado la changuita. 😕\n\n"
                    f"📌 Motivo de la cancelación:\n"
                    f"\"{motivo}\"\n\n"
                    f"🙏 Gracias por usar ChangApp. Si tenés alguna duda o problema, no dudes en contactarnos.\n\n"
                    f"Saludos,\n"
                    f"El equipo de ChangApp."
                )
            )

            # Enviar email con motivo personalizado
            email_destino = destino.email if destino and destino.email else None
            if email_destino:
                asunto = "Una changuita fue cancelada"
                cuerpo = (
                    f"👋 Hola {destino.first_name} {destino.last_name},\n\n"
                    f"Lamentamos informarte que {usuario_actual.first_name} {usuario_actual.last_name} ha cancelado el servicio solicitado. 😕\n\n"
                    f"📌 Motivo de la cancelación:\n"
                    f"\"{motivo}\"\n\n"
                    f"Te recomendamos estar atento a nuevas oportunidades en la plataforma.\n\n"
                    f"🙏 Gracias por usar ChangApp. Si tenés alguna duda o problema, no dudes en contactarnos.\n\n"
                    f"Saludos,\n"
                    f"El equipo de ChangApp."
                )
                send_mail(
                    subject=asunto,
                    message=cuerpo,
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