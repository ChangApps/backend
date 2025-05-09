from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from ChangApp.servicio.models.proveedorServicioModels import ProveedorServicio
from ChangApp.servicio.serializers.proveedorServicioSerializer import ProveedorServicioSerializer

class ProveedorServicioPorUsuarioView(viewsets.ViewSet):
    def get_proveedor_servicio_by_user(self, request, user_id=None):
        try:
            # Filtrar por el ID del proveedor (usuario)
            proveedor_servicio = ProveedorServicio.objects.filter(proveedor__id=user_id)
            # Si no se encuentran resultados
            if not proveedor_servicio:
                return Response({'detail': 'ProveedorServicio no encontrado para este usuario'}, status=status.HTTP_404_NOT_FOUND)
            # Serializar los resultados
            serializer = ProveedorServicioSerializer(proveedor_servicio, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)