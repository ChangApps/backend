from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from ChangApp.solicitud.models import Solicitud

class AceptarChanguitaView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        solicitud_id = request.data.get("solicitud_id")

        try:
            solicitud = Solicitud.objects.get(id=solicitud_id)

            # Validar que el proveedor actual sea el que fue asignado
            if solicitud.proveedorServicio.proveedor != request.user:
                return Response({"error": "No sos el proveedor asignado."}, status=403)

            # Cambiar estado a iniciado
            solicitud.estado = 'I'  # 'Iniciado'
            solicitud.save()

            return Response({"success": "Changuita aceptada y comenzada."}, status=200)

        except Solicitud.DoesNotExist:
            return Response({"error": "Solicitud no encontrada."}, status=404)
