from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ChangApp.servicio.models.proveedorServicioModels import ProveedorServicio

class VerificarProveedorServicioView(APIView):
    def get(self, request, user_id, servicio_id):
        try:
            # Filtrar por usuario y servicio
            proveedor_servicio = ProveedorServicio.objects.filter(proveedor_id=user_id, servicio_id=servicio_id).first()
            if proveedor_servicio:
                return Response({"id": proveedor_servicio.id}, status=status.HTTP_200_OK)
            else:
                return Response({"detail": "No se encontró un ProveedorServicio para este usuario con ese servicio"},
                                status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)