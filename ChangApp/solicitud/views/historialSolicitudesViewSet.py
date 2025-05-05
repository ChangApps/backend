from rest_framework import viewsets, status
from rest_framework.response import Response
from ChangApp.solicitud.models import Solicitud
from ChangApp.solicitud.serializers.solicitudSerializer import SolicitudSerializer

class HistorialSolicitudesViewSet(viewsets.ViewSet):
    def get_solicitudes_cliente(self, request, *args, **kwargs):
        usuario_id = self.kwargs.get("usuario_id") 
        
        if not usuario_id:
            return Response({"error": "Debe proporcionar un ID de usuario"}, status=status.HTTP_400_BAD_REQUEST)
        
        # obtiene el historial desde el modelo, filtrado por usuario_id
        print('usuario_id es cliente',usuario_id)
        historial = Solicitud.objects.filter(cliente_id=usuario_id)
        
        if not historial.exists():
            return Response({"error": "No se encontraron solicitudes para este usuario"}, status=status.HTTP_404_NOT_FOUND)
        
        # usamos el serializer para convertir los objetos en una respuesta JSON 
        serializer = SolicitudSerializer(historial, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def get_solicitudes_proveedor(self, request, *args, **kwargs):
        usuario_id = self.kwargs.get("usuario_id") 
        
        if not usuario_id:
            return Response({"error": "Debe proporcionar un ID de usuario"}, status=status.HTTP_400_BAD_REQUEST)
        
        # obtiene el historial desde el modelo, filtrado por usuario_id
        print('usuario_id es proveedor',usuario_id)
        historial = Solicitud.objects.filter(proveedorServicio__proveedor=usuario_id)
        
        if not historial.exists():
            return Response({"error": "No se encontraron solicitudes para este usuario"}, status=status.HTTP_404_NOT_FOUND)
        
        # usamos el serializer para convertir los objetos en una respuesta JSON 
        serializer = SolicitudSerializer(historial, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)