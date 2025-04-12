from rest_framework import status, viewsets
from rest_framework.response import Response
from ChangApp.solicitud.models import Solicitud
from rest_framework.decorators import action
from ChangApp.solicitud.serializers.solicitudSerializer import SolicitudSerializer

class SolicitudViewSet(viewsets.ModelViewSet):
    queryset = Solicitud.objects.all()
    serializer_class = SolicitudSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            solicitud = serializer.save()  # Ahora el serializer maneja la creación
            return Response(SolicitudSerializer(solicitud).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
       # Método que recibe el proveedor_id y devuelve las solicitudes que coinciden (requerida para las resenias)
    @action(detail=False, methods=['get'], url_path='por-proveedor/(?P<proveedor_id>[^/.]+)')
    def por_proveedor(self, request, proveedor_id=None):
        try:
            # Filtramos las solicitudes por proveedor_id
            solicitudes = Solicitud.objects.filter(proveedorServicio__proveedor__id=proveedor_id)

            if not solicitudes:
                return Response({"message": "No se encontraron solicitudes para este proveedor."}, status=status.HTTP_404_NOT_FOUND)

            # Serializamos las solicitudes
            serializer = SolicitudSerializer(solicitudes, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Solicitud.DoesNotExist:
            return Response({'error': 'Solicitudes no encontradas para este proveedor'}, status=status.HTTP_404_NOT_FOUND)