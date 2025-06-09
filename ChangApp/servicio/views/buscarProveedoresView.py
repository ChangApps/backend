# Importaciones necesarias de DRF, modelos, utilidades y Swagger
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ChangApp.servicio.models.servicioModels import Servicio, HorarioServicio
from datetime import time
from django.db.models import Q
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class BuscarProveedoresAPIView(APIView):
    # Documentación Swagger para los parámetros y respuestas
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
                description="Lista de días (ej: Lunes, Martes, etc.)",
                type=openapi.TYPE_STRING,
                required=True,
                multiple=True
            ),
            openapi.Parameter(
                'desde_horas[]',
                openapi.IN_QUERY,
                description="Lista de horas de inicio (formato HH:MM o HH:MM:SS)",
                type=openapi.TYPE_STRING,
                required=True,
                multiple=True
            ),
            openapi.Parameter(
                'hasta_horas[]',
                openapi.IN_QUERY,
                description="Lista de horas de fin (formato HH:MM o HH:MM:SS)",
                type=openapi.TYPE_STRING,
                required=True,
                multiple=True
            ),
        ],
        responses={
            200: openapi.Response(description="Lista de proveedores disponibles"),
            400: "Error en los parámetros",
            404: "No se encontraron servicios",
            500: "Error interno del servidor"
        }
    )
    def get(self, request, *args, **kwargs):
        # Obtener parámetros desde el query string
        nombre_servicio = request.query_params.get('nombre_servicio')
        dias = request.query_params.getlist('dias[]')
        desde_horas = request.query_params.getlist('desde_horas[]')
        hasta_horas = request.query_params.getlist('hasta_horas[]')

        # Validación básica de parámetros
        if not nombre_servicio:
            return Response({"error": "Debe proporcionar el nombre del servicio"}, status=status.HTTP_400_BAD_REQUEST)

        if not dias or not desde_horas or not hasta_horas:
            return Response({"error": "Debe proporcionar listas de días, horas desde y horas hasta"}, status=status.HTTP_400_BAD_REQUEST)

        if len(dias) != len(desde_horas) or len(dias) != len(hasta_horas):
            return Response({"error": "Las listas de días, horas desde y horas hasta deben tener la misma longitud"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            filtros = Q()  # Acumulador de condiciones OR

            # Recorrer cada rango horario para construir los filtros
            for i in range(len(dias)):
                dia = dias[i]
                desde_str = desde_horas[i]
                hasta_str = hasta_horas[i]

                # Asegurar formato HH:MM:SS
                if len(desde_str.split(':')) == 2:
                    desde_str += ':00'
                if len(hasta_str.split(':')) == 2:
                    hasta_str += ':00'

                # Convertir a objetos time
                desde_time = time.fromisoformat(desde_str)
                hasta_time = time.fromisoformat(hasta_str)

                # Validar que la hora de inicio sea menor que la de fin
                if desde_time >= hasta_time:
                    return Response({"error": f"La hora de inicio debe ser menor que la hora de fin para {dia}"}, status=status.HTTP_400_BAD_REQUEST)

                # Agregar condición al filtro compuesto (OR entre todas)
                filtros |= Q(
                    servicio__nombreServicio=nombre_servicio,
                    dia=dia,
                    desdeHora__lt=hasta_time,
                    hastaHora__gt=desde_time
                )

            # Buscar horarios que cumplan con alguno de los filtros
            horarios = HorarioServicio.objects.filter(filtros).select_related('servicio').distinct()

            # Si no hay horarios que coincidan, responder con 404
            if not horarios.exists():
                horarios_str = ", ".join([f"{dias[i]} ({desde_horas[i]} - {hasta_horas[i]})" for i in range(len(dias))])
                return Response({"error": f"No se encontraron servicios '{nombre_servicio}' en los horarios: {horarios_str}"}, status=status.HTTP_404_NOT_FOUND)

            proveedores_data = []  # Lista para acumular proveedores

            # Recorrer los horarios encontrados
            for horario in horarios:
                servicio = horario.servicio
                # Para cada servicio en el horario, obtener los proveedores asociados
                for proveedor in servicio.obtener_proveedores():
                    proveedores_data.append({
                        "id": proveedor.id,
                        "username": proveedor.username,
                        "nombre": proveedor.first_name,
                        "apellido": proveedor.last_name,
                        "email": proveedor.email,
                        "puntaje": getattr(proveedor, 'puntaje', None),
                        "fotoPerfil": proveedor.fotoPerfil.url if getattr(proveedor, 'fotoPerfil', None) else None,
                        "nombreServicio": servicio.nombreServicio,
                        "idServicio": servicio.id,
                        "dia": horario.dia,
                        "desdeHora": str(horario.desdeHora),
                        "hastaHora": str(horario.hastaHora)
                    })

            # Devolver la lista de proveedores encontrados
            return Response({"proveedores": proveedores_data}, status=status.HTTP_200_OK)

        except Exception as e:
            # Capturar errores inesperados y devolver 500
            return Response({"error": f"Error interno del servidor: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
