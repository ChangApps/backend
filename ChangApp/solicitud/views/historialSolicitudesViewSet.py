from rest_framework import viewsets, status
from rest_framework.response import Response
from ChangApp.solicitud.models import Solicitud
from ChangApp.solicitud.serializers.solicitudSerializer import SolicitudSerializer

class HistorialSolicitudesViewSet(viewsets.ViewSet):
    def get_solicitudes_cliente(self, request, *args, **kwargs):
        usuario_id = self.kwargs.get("usuario_id") 
        
        if not usuario_id:
            return Response({"error": "Debe proporcionar un ID de usuario"}, status=status.HTTP_400_BAD_REQUEST)
        
        # obtiene el historial (solicitudes donde soy cliente) desde el modelo, filtrado por usuario_id
        historial = Solicitud.objects.filter(cliente_id=usuario_id)
        
        if not historial.exists():
            return Response({
                "message": "No se encontraron solicitudes para este usuario donde sea cliente",
                "data": []
            }, status=status.HTTP_200_OK) #cambie BAD_REQUEST_404 por HTTP_202 porque tiraba error de url, cuando en realidad el post estaba bien hecho
        
        # usamos el serializer para convertir los objetos en una respuesta JSON 
        serializer = SolicitudSerializer(historial, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def get_solicitudes_proveedor(self, request, *args, **kwargs):
        usuario_id = self.kwargs.get("usuario_id")
        if not usuario_id:
            return Response({"error": "Debe proporcionar un ID de usuario"}, status=status.HTTP_400_BAD_REQUEST)
        
        # obtiene el historial (solicitudes donde soy proveedor) desde el modelo, filtrado por usuario_id
        historial = Solicitud.objects.filter(proveedorServicio__proveedor=usuario_id)
        
        if not historial.exists():
            return Response({
                "message": "No se encontraron solicitudes para este usuario donde sea proveedor",
                "data": []
            }, status=status.HTTP_200_OK)
        
        # usamos el serializer para convertir los objetos en una respuesta JSON 
        serializer = SolicitudSerializer(historial, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)