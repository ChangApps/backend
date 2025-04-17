from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ChangApp.servicio.models.servicioModels import Servicio

class BuscarProveedoresAPIView(APIView):
    def get(self, request, *args, **kwargs):
        nombre_servicio = request.query_params.get('nombre_servicio', None)
        dias = request.query_params.getlist('dias', [])  # Permite recibir múltiples días
        
        if not nombre_servicio:
            return Response({"error": "Debe proporcionar el nombre del servicio"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            servicios = Servicio.objects.filter(nombreServicio=nombre_servicio)
            
            if dias:
                servicios = servicios.filter(dia__in=dias)  # Filtrar por los días si se proporcionan
            
            if not servicios.exists():
                return Response({"error": "No se encontraron servicios con los criterios proporcionados"}, status=status.HTTP_404_NOT_FOUND)
            
            proveedores_data = []
            for servicio in servicios:
                for proveedor in servicio.obtener_proveedores():
                    proveedores_data.append({
                        "id": proveedor.id,
                        "username": proveedor.username,
                        "nombre": proveedor.first_name,
                        "apellido": proveedor.last_name,
                        "email": proveedor.email,
                        "puntaje": proveedor.puntaje,
                        "fotoPerfil": proveedor.fotoPerfil.url if proveedor.fotoPerfil else None,
                        "nombreServicio": servicio.nombreServicio,
                        "idServicio": servicio.id, 
                        "dia": servicio.dia,
                        "desdeHora": servicio.desdeHora,
                        "hastaHora": servicio.hastaHora,
                    })
            
            return Response({"proveedores": proveedores_data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)