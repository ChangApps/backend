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
        return ProveedorServicio.objects.filter(
            proveedor_id=user_id, servicio_id=servicio_id
        ).first()
    except Exception:
        return None


class BuscarUsuarioViewSet(viewsets.ModelViewSet):
    serializer_class = BuscarUsuarioSerializer

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "q",
                openapi.IN_QUERY,
                description="Texto para buscar por nombre, apellido, username o servicio",
                type=openapi.TYPE_STRING,
            )
        ]
    )
    @action(detail=False, methods=["get"])
    def buscar(self, request):
        q = request.query_params.get("q", None)
        usuario_actual = request.user

        if not q:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        q_lower = q.lower()
        nombres = q_lower.split()

        # Buscar coincidencias de servicios por nombre
        servicios_coincidentes = ProveedorServicio.objects.filter(
            servicio__nombreServicio__icontains=q_lower
        ).values_list("servicio__id", flat=True).distinct()

        # Query base excluyendo usuario actual y bloqueados
        queryset = ProveedorServicio.objects.exclude(
            proveedor=usuario_actual
        ).exclude(
            Q(proveedor__in=usuario_actual.bloqueados.all())
            | Q(proveedor__bloqueados=usuario_actual)
        )

        # Construir Q dinámico para nombre, apellido y username
        q_filter = Q(proveedor__username__icontains=q_lower) | Q(servicio__nombreServicio__icontains=q_lower)

        if len(nombres) == 1:
            # Solo un token → puede ser nombre, apellido o username
            q_filter |= Q(proveedor__first_name__icontains=nombres[0]) | Q(proveedor__last_name__icontains=nombres[0])
        elif len(nombres) >= 2:
            # Más de un token → buscar combinación first_name + last_name
            q_filter |= Q(proveedor__first_name__icontains=nombres[0], proveedor__last_name__icontains=nombres[1])

        queryset = queryset.filter(q_filter).distinct()

        # Agrupar resultados por proveedor
        servicios_por_proveedor = {}

        for ps in queryset:
            verificado = obtener_proveedor_servicio_por_usuario_y_servicio(
                ps.proveedor.id, ps.servicio.id
            )
            if not verificado:
                continue

            proveedor_id = ps.proveedor.id

            if proveedor_id not in servicios_por_proveedor:
                servicios_por_proveedor[proveedor_id] = {
                    "proveedor": ps.proveedor,
                    "servicios": [],
                }

            # Si buscó por username o nombre/apellido → traer todos los servicios del proveedor
            if (
                ps.proveedor.username.lower().find(q_lower) != -1
                or ps.proveedor.first_name.lower().find(nombres[0]) != -1
                or ps.proveedor.last_name.lower().find(nombres[0]) != -1
            ):
                servicios_por_proveedor[proveedor_id]["servicios"] = list(
                    Servicio.objects.filter(
                        proveedores_servicio__proveedor=ps.proveedor
                    ).distinct()
                )
            # Si buscó por nombre de servicio → solo ese servicio
            elif ps.servicio.id in servicios_coincidentes:
                servicios_por_proveedor[proveedor_id]["servicios"].append(ps.servicio)

        if not servicios_por_proveedor:
            return Response(status=status.HTTP_204_NO_CONTENT)

        # Preparar datos para el serializer
        datos_serializables = [
            {
                "proveedor": entry["proveedor"],
                "servicios": entry["servicios"],
            }
            for entry in servicios_por_proveedor.values()
        ]

        serializer = BuscarUsuarioSerializer(datos_serializables, many=True)
        return Response(serializer.data)