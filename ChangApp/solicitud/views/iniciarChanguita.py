from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from ChangApp.servicio.models.proveedorServicioModels import ProveedorServicio
from ChangApp.solicitud.models import EstadoServicio, Solicitud
from ChangApp.notificacion.models import Notificacion
from django.core.mail import send_mail
from django.conf import settings

class IniciarChanguitaView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Inicia una changuita: el cliente selecciona un proveedor",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['proveedor_id'],
            properties={
                'proveedor_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID del ProveedorServicio seleccionado'),
            },
        ),
        responses={201: 'Solicitud creada correctamente'}
    )

    def post(self, request):
        proveedor_id = request.data.get("proveedorServicio")
        
        try:
            proveedor_servicio = ProveedorServicio.objects.get(id=proveedor_id)
            proveedor = proveedor_servicio.proveedor
            cliente = request.user
            categorias_servicio = proveedor_servicio.servicio.categorias.all()

            # Verificar si el cliente ya tiene una solicitud activa en alguna de esas categorías
            solicitud_existente = Solicitud.objects.filter(
                cliente=cliente,
                estado__in=[
                    EstadoServicio.PENDIENTE_ACEPTACION,
                    EstadoServicio.INICIADO,
                ],
                proveedorServicio__servicio__categorias__in=categorias_servicio
            ).distinct().exists() # Agrego distinct() para evitar devolver duplicados por combinaciones de relaciones 

            if solicitud_existente:
                return Response(
                    {"error": "Ya tenés una changuita activa en esta categoría. Finalizala antes de contratar otro proveedor."},
                    status=400
                )

             # Crear la solicitud
            solicitud = Solicitud.objects.create(
                cliente=cliente,
                proveedorServicio=proveedor_servicio,
                estado=EstadoServicio.PENDIENTE_ACEPTACION
            )
            solicitud.save()

               # Mensaje con información del cliente
            mensaje = (
                f"Hola {proveedor.first_name} {proveedor.last_name}!\n\n"
                f"{cliente.first_name} {cliente.last_name} "
                f"desea contratarte para una changuita. 💼\n\n"
                f"Por favor, ingresá a la app para aceptar o rechazar la solicitud.\n\n"
                f"Saludos,\n"
                f"El equipo de ChangApp"
            )
            Notificacion.objects.create(
                usuario_destino=proveedor,
                notificacion_de_sistema=False,
                mensaje=mensaje
            )
            
            # Enviar email al proveedor
            if proveedor.email:
                send_mail(
                    subject='Nueva solicitud de changuita',
                    message=mensaje,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[proveedor.email],
                    fail_silently=False,
                )

            return Response({"success": "Solicitud iniciada. Notificación enviada al proveedor.",
                             "id_solicitud": solicitud.id,
                             "email_destino":proveedor.email,
                             },
                             status=200)

        except ProveedorServicio.DoesNotExist:
            return Response({"error": "Proveedor no encontrado."}, status=404)
        except Solicitud.DoesNotExist:
            return Response({"error": "Solicitud no encontrada o no sos el dueño."}, status=404)