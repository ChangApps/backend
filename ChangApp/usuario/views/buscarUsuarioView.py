from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.db.models import Q
from ChangApp.servicio.models import ProveedorServicio
from ChangApp.servicio.models.servicioModels import Servicio
from ChangApp.usuario.serializers.buscarUsuarioSerializer import BuscarUsuarioSerializer

def obtener_proveedor_servicio_por_usuario_y_servicio(user_id, servicio_id):
    try:
        return ProveedorServicio.objects.filter(proveedor_id=user_id, servicio_id=servicio_id).first()
    except Exception:
        return None

class BuscarUsuarioViewSet(viewsets.ModelViewSet):
    serializer_class = BuscarUsuarioSerializer

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'q',
                openapi.IN_QUERY,
                description="Texto para buscar por nombre, apellido o servicio",
                type=openapi.TYPE_STRING
            )
        ]
    )
    @action(detail=False, methods=['get'])
    def buscar(self, request):
        q = request.query_params.get('q', None)
        usuario_actual = request.user
        resultados = []

        if not q:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        q_lower = q.lower()

        # Averiguar si coincide con algún nombre de servicio
        servicios_coincidentes = ProveedorServicio.objects.filter(
            Q(servicio__nombreServicio__icontains=q_lower)
        ).values_list('servicio__id', flat=True).distinct()

        queryset = ProveedorServicio.objects.filter(
            (
                Q(proveedor__username__icontains=q) |
                Q(proveedor__first_name__icontains=q) |
                Q(proveedor__last_name__icontains=q) |
                Q(servicio__nombreServicio__icontains=q)
            ) & ~Q(proveedor=usuario_actual)
        ).distinct()

        # Agrupar resultados
        servicios_por_proveedor = {}

        for ps in queryset:
            verificado = obtener_proveedor_servicio_por_usuario_y_servicio(ps.proveedor.id, ps.servicio.id)
            if not verificado:
                continue

            proveedor_id = ps.proveedor.id

            # Si no existe, inicializamos la entrada
            if proveedor_id not in servicios_por_proveedor:
                servicios_por_proveedor[proveedor_id] = {
                    'proveedor': ps.proveedor,
                    'servicios': []
                }

            # Si buscó por nombre/apellido → agregamos todos los servicios
            if ps.proveedor.first_name.lower().find(q_lower) != -1 or ps.proveedor.last_name.lower().find(q_lower) != -1:
                servicios_por_proveedor[proveedor_id]['servicios'] = Servicio.objects.filter(
                    proveedores_servicio__proveedor=ps.proveedor
                ).distinct()
            else:
                # Si buscó por nombre de servicio → solo ese servicio
                if ps.servicio.id in servicios_coincidentes:
                    servicios_por_proveedor[proveedor_id]['servicios'].append(ps.servicio)

        if not servicios_por_proveedor:
            return Response(status=status.HTTP_204_NO_CONTENT)

        datos_serializables = [
            {
                'proveedor': entry['proveedor'],
                'servicios': entry['servicios']
            }
            for entry in servicios_por_proveedor.values()
        ]

        serializer = BuscarUsuarioSerializer(datos_serializables, many=True)
        return Response(serializer.data)