from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from ChangApp.servicio.models.proveedorServicioModels import ProveedorServicio
from ChangApp.solicitud.models import Solicitud
from ChangApp.notificacion.models import Notificacion

class IniciarChanguitaView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        proveedor_id = request.data.get("proveedor_id")
        solicitud_id = request.data.get("solicitud_id")

        try:
            proveedor_servicio = ProveedorServicio.objects.get(id=proveedor_id)
            proveedor = proveedor_servicio.proveedor

            solicitud = Solicitud.objects.get(id=solicitud_id, cliente=request.user)

            solicitud.proveedorServicio = proveedor_servicio
            solicitud.estado = 'PENDIENTE_ACEPTACION'
            solicitud.save()

            mensaje = f"{request.user.username} quiere contratarte para una changuita. ¿Aceptás?"
            Notificacion.objects.create(
                usuario=proveedor,
                mensaje=mensaje
            )

            return Response({"success": "Solicitud iniciada. Notificación enviada al proveedor."}, status=200)

        except ProveedorServicio.DoesNotExist:
            return Response({"error": "Proveedor no encontrado."}, status=404)
        except Solicitud.DoesNotExist:
            return Response({"error": "Solicitud no encontrada o no sos el dueño."}, status=404)
