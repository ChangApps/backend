from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ChangApp.servicio.models.servicioModels import Servicio
from datetime import time

class BuscarProveedoresAPIView(APIView):
    def get(self, request, *args, **kwargs):
        nombre_servicio = request.query_params.get('nombre_servicio', None)
        dias = request.query_params.getlist('dias', [])  # Permite recibir múltiples días
        desde_hora = request.query_params.get('desdeHora', None)
        hasta_hora = request.query_params.get('hastaHora', None)

        if not nombre_servicio:
            return Response({"error": "Debe proporcionar el nombre del servicio"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Validar que si se pasan horarios, estén correctos
        if (desde_hora and not hasta_hora) or (hasta_hora and not desde_hora):
            return Response({"error": "Debe proporcionar tanto desdeHora como hastaHora"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            if desde_hora and hasta_hora:
                try:
                    # Intentamos convertir strings a objetos time
                    desde_hora_obj = time.fromisoformat(desde_hora)
                    hasta_hora_obj = time.fromisoformat(hasta_hora)
                except ValueError:
                    return Response({"error": "Formato de hora inválido. Use HH:MM"}, status=status.HTTP_400_BAD_REQUEST)

                if desde_hora_obj >= hasta_hora_obj:
                    return Response({"error": "La hora de inicio debe ser menor que la hora de fin"}, status=status.HTTP_400_BAD_REQUEST)
            
            servicios = Servicio.objects.filter(nombreServicio=nombre_servicio)
            
            if dias:
                servicios = servicios.filter(dia__in=dias)

            if desde_hora and hasta_hora:
                # Buscar servicios que se solapen
                servicios = servicios.filter(
                    desdeHora__lt=hasta_hora_obj,
                    hastaHora__gt=desde_hora_obj
                )
                
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