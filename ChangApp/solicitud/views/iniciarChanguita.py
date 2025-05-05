from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from ChangApp.servicio.models.proveedorServicioModels import ProveedorServicio
from ChangApp.solicitud.models import EstadoServicio, Solicitud
from ChangApp.notificacion.models import Notificacion

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

             # Crear la solicitud
            solicitud = Solicitud.objects.create(
                cliente=cliente,
                proveedorServicio=proveedor_servicio,
                estado=EstadoServicio.PENDIENTE_ACEPTACION
            )
            solicitud.save()

            mensaje = f"{request.user.username} quiere contratarte para una changuita. ¿Aceptás?"
            Notificacion.objects.create(
                usuario_destino=proveedor,
                notificacion_de_sistema=False,
                mensaje=mensaje
            )

            return Response({"success": "Solicitud iniciada. Notificación enviada al proveedor."}, status=200)

        except ProveedorServicio.DoesNotExist:
            return Response({"error": "Proveedor no encontrado."}, status=404)
        except Solicitud.DoesNotExist:
            return Response({"error": "Solicitud no encontrada o no sos el dueño."}, status=404)
