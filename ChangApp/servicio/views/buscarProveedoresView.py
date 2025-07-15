from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from datetime import time
from django.db.models import Q
from ChangApp.servicio.models.servicioModels import HorarioServicio

class BuscarProveedoresAPIView(APIView):
    #Documentación Swagger para la de búsqueda de proveedores
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
        nombre_servicio = request.query_params.get('nombre_servicio')
        dias = request.query_params.getlist('dias[]')
        desde_horas = request.query_params.getlist('desde_horas[]')
        hasta_horas = request.query_params.getlist('hasta_horas[]')

        if not nombre_servicio:
            return Response({"error": "Debe proporcionar el nombre del servicio"}, status=status.HTTP_400_BAD_REQUEST)

        if not dias or not desde_horas or not hasta_horas:
            return Response({"error": "Debe proporcionar listas de días, horas desde y horas hasta"}, status=status.HTTP_400_BAD_REQUEST)

        if len(dias) != len(desde_horas) or len(dias) != len(hasta_horas):
            return Response({"error": "Las listas de días, horas desde y horas hasta deben tener la misma longitud"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            filtros = Q()

            for i in range(len(dias)):
                dia = dias[i]
                desde_str = desde_horas[i]
                hasta_str = hasta_horas[i]

                if len(desde_str.split(':')) == 2:
                    desde_str += ':00'
                if len(hasta_str.split(':')) == 2:
                    hasta_str += ':00'

                desde_time = time.fromisoformat(desde_str)
                hasta_time = time.fromisoformat(hasta_str)

                if desde_time >= hasta_time:
                    return Response({"error": f"La hora de inicio debe ser menor que la de fin para {dia}"}, status=status.HTTP_400_BAD_REQUEST)

                filtros |= Q(
                    servicio__nombreServicio=nombre_servicio,
                    dia=dia,
                    desdeHora__lt=hasta_time,
                    hastaHora__gt=desde_time
                )

            horarios = HorarioServicio.objects.filter(filtros).select_related('servicio').distinct()

            if not horarios.exists():
                horarios_str = ", ".join([f"{dias[i]} ({desde_horas[i]} - {hasta_horas[i]})" for i in range(len(dias))])
                return Response({"error": f"No se encontraron servicios '{nombre_servicio}' en los horarios: {horarios_str}"}, status=status.HTTP_404_NOT_FOUND)

            # Agrupar por proveedor y servicio
            agrupados = {}

            for horario in horarios:
                servicio = horario.servicio
                for proveedor in servicio.obtener_proveedores():
                    key = (proveedor.id, servicio.id)

                    if key not in agrupados:
                        agrupados[key] = {
                            "id": proveedor.id,
                            "username": proveedor.username,
                            "nombre": proveedor.first_name,
                            "apellido": proveedor.last_name,
                            "email": proveedor.email,
                            "puntaje": getattr(proveedor, 'puntaje', None),
                            "fotoPerfil": proveedor.fotoPerfil.url if getattr(proveedor, 'fotoPerfil', None) else None,
                            "nombreServicio": servicio.nombreServicio,
                            "idServicio": servicio.id,
                            "dias": []
                        }

                    agrupados[key]["dias"].append({
                        "dia": horario.dia,
                        "desdeHora": str(horario.desdeHora),
                        "hastaHora": str(horario.hastaHora)
                    })

            proveedores_data = list(agrupados.values())
            return Response({"proveedores": proveedores_data}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": f"Error interno del servidor: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
