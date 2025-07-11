from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.db.models import Q
from ChangApp.servicio.models import ProveedorServicio
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

        if q:
            queryset = ProveedorServicio.objects.filter(
                (Q(proveedor__first_name__icontains=q) |
                Q(proveedor__last_name__icontains=q) |
                Q(servicio__nombreServicio__icontains=q)) &
                ~Q(proveedor=usuario_actual)  # Excluir usuario actual
            ).distinct()
        else:
            queryset = ProveedorServicio.objects.exclude(proveedor=usuario_actual)

        resultados = []

        for ps in queryset:
            verificado = obtener_proveedor_servicio_por_usuario_y_servicio(ps.proveedor.id, ps.servicio.id)
            if verificado:
                resultados.append(ps)

        if not resultados:
            return Response(status=status.HTTP_204_NO_CONTENT)

        serializer = BuscarUsuarioSerializer(resultados, many=True)
        return Response(serializer.data)
