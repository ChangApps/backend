from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ChangApp.servicio.models.servicioModels import Servicio
from datetime import time
from django.db.models import Q
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class BuscarProveedoresAPIView(APIView):
     @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'nombre_servicio',
                openapi.IN_QUERY,
                description="Nombre del servicio a buscar",
                type=openapi.TYPE_STRING,
                required=True
            ),
            openapi.Parameter(
                'dias[]',
                openapi.IN_QUERY,
                description="Lista de días (ej: lunes, martes, etc.)",
                type=openapi.TYPE_STRING,
                required=True,
                multiple=True
            ),
            openapi.Parameter(
                'desde_horas[]',
                openapi.IN_QUERY,
                description="Lista de horas de inicio (formato HH:MM:SS)",
                type=openapi.TYPE_STRING,
                required=True,
                multiple=True
            ),
            openapi.Parameter(
                'hasta_horas[]',
                openapi.IN_QUERY,
                description="Lista de horas de fin (formato HH:MM:SS)",
                type=openapi.TYPE_STRING,
                required=True,
                multiple=True
            )
        ],
        responses={
            200: openapi.Response(description="Lista de proveedores disponibles"),
            400: "Error en los parámetros",
            404: "No se encontraron servicios",
            500: "Error interno del servidor"
        }
    )
     def get(self, request, *args, **kwargs):
        nombre_servicio = request.query_params.get('nombre_servicio', None)
        dias = request.query_params.getlist('dias[]', [])
        desde_horas = request.query_params.getlist('desde_horas[]', [])
        hasta_horas = request.query_params.getlist('hasta_horas[]', [])
        
        if not nombre_servicio:
            return Response({"error": "Debe proporcionar el nombre del servicio"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Validar que todos los arrays tengan la misma longitud
        if len(dias) != len(desde_horas) or len(dias) != len(hasta_horas):
            return Response({
                "error": "Los arrays de días, horas de inicio y horas de fin deben tener la misma longitud"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        if not dias:
            return Response({"error": "Debe proporcionar al menos un día"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # Procesar cada día con su horario específico
            consultas_por_dia = []
            
            for i in range(len(dias)):
                dia = dias[i]
                desde_hora = desde_horas[i]
                hasta_hora = hasta_horas[i]
                
                try:
                    # Manejar tanto formato HH:MM:SS como HH:MM
                    if len(desde_hora.split(':')) == 3:
                        desde_hora_str = desde_hora
                    else:
                        desde_hora_str = desde_hora + ':00'
                    
                    if len(hasta_hora.split(':')) == 3:
                        hasta_hora_str = hasta_hora
                    else:
                        hasta_hora_str = hasta_hora + ':00'
                    
                    # Convertir strings a objetos time
                    desde_hora_obj = time.fromisoformat(desde_hora_str)
                    hasta_hora_obj = time.fromisoformat(hasta_hora_str)
                    
                    if desde_hora_obj >= hasta_hora_obj:
                        return Response({
                            "error": f"La hora de inicio debe ser menor que la hora de fin para {dia}"
                        }, status=status.HTTP_400_BAD_REQUEST)
                    
                    # Crear consulta para este día específico con su horario
                    # Un servicio coincide si:
                    # 1. Es el día correcto
                    # 2. Hay solapamiento de horarios (su inicio < nuestro fin Y su fin > nuestro inicio)
                    consulta_dia = Q(
                        nombreServicio=nombre_servicio,
                        dia=dia,
                        desdeHora__lt=hasta_hora_obj,  # Su hora de inicio es antes de nuestra hora de fin
                        hastaHora__gt=desde_hora_obj   # Su hora de fin es después de nuestra hora de inicio
                    )
                    
                    consultas_por_dia.append(consulta_dia)
                    
                except ValueError as ve:
                    return Response({
                        "error": f"Formato de hora inválido para {dia}. Use HH:MM o HH:MM:SS. Error: {str(ve)}"
                    }, status=status.HTTP_400_BAD_REQUEST)
            
            # Combinar todas las consultas con OR (al menos una debe cumplirse)
            consulta_final = consultas_por_dia[0]
            for consulta in consultas_por_dia[1:]:
                consulta_final |= consulta
            
            # Ejecutar la consulta
            servicios = Servicio.objects.filter(consulta_final)
            
            if not servicios.exists():
                horarios_info = []
                for i in range(len(dias)):
                    horarios_info.append(f"{dias[i]} ({desde_horas[i]}-{hasta_horas[i]})")
                
                return Response({
                    "error": f"No se encontraron servicios para '{nombre_servicio}' en los horarios: {', '.join(horarios_info)}"
                }, status=status.HTTP_404_NOT_FOUND)
            
            # Construir la respuesta con información de los proveedores
            proveedores_data = []
            proveedores_ids_agregados = set()  # Para evitar duplicados del mismo proveedor
            
            for servicio in servicios:
                for proveedor in servicio.obtener_proveedores():
                    # Evitar duplicados del mismo proveedor
                    if proveedor.id not in proveedores_ids_agregados:
                        proveedores_ids_agregados.add(proveedor.id)
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
                            "desdeHora": str(servicio.desdeHora),
                            "hastaHora": str(servicio.hastaHora),
                        })
            
            return Response({"proveedores": proveedores_data}, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({
                "error": f"Error interno del servidor: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)