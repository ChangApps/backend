from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from ChangApp.solicitud.models import Solicitud

class RechazarChanguitaView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        solicitud_id = request.data.get("solicitud_id")

        try:
            solicitud = Solicitud.objects.get(id=solicitud_id)

            if solicitud.proveedorServicio.proveedor != request.user:
                return Response({"error": "No sos el proveedor asignado."}, status=403)

            # Rechaza: elimina proveedor y vuelve al estado inicial
            solicitud.proveedorServicio = None
            solicitud.estado = 'C'  # Cancelado o volvés a un estado anterior
            solicitud.save()

            return Response({"success": "Changuita rechazada."}, status=200)

        except Solicitud.DoesNotExist:
            return Response({"error": "Solicitud no encontrada."}, status=404)
