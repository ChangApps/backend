from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.db.models import Q
from ChangApp.servicio.models import ProveedorServicio
from ChangApp.servicio.models.servicioModels import Servicio
from ChangApp.usuario.serializers.buscarUsuarioSerializer import BuscarUsuarioSerializer
import unicodedata


def obtener_proveedor_servicio_por_usuario_y_servicio(user_id, servicio_id):
    try:
        return ProveedorServicio.objects.filter(
            proveedor_id=user_id, servicio_id=servicio_id
        ).first()
    except Exception:
        return None
    
def normalize_text(text: str) -> str:
    """Convierte en minúsculas y elimina acentos/tildes"""
    if not text:
        return ""
    text = text.lower()
    return ''.join(
        c for c in unicodedata.normalize('NFD', text)
        if unicodedata.category(c) != 'Mn'
    )

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

        q_norm = normalize_text(q)
        nombres_norm = q_norm.split()

        # Query base excluyendo usuario actual y bloqueados
        queryset = ProveedorServicio.objects.exclude(
            proveedor=usuario_actual
        ).exclude(
            Q(proveedor__in=usuario_actual.bloqueados.all()) |
            Q(proveedor__bloqueados=usuario_actual)
        )

        servicios_por_proveedor = {}

        for ps in queryset:
            # Normalizar campos
            proveedor_norm = normalize_text(f"{ps.proveedor.first_name} {ps.proveedor.last_name} {ps.proveedor.username}")
            servicio_norm = normalize_text(ps.servicio.nombreServicio)

            # Verificar match
            if q_norm in proveedor_norm or q_norm in servicio_norm:
                if not obtener_proveedor_servicio_por_usuario_y_servicio(ps.proveedor.id, ps.servicio.id):
                    continue

                pid = ps.proveedor.id
                if pid not in servicios_por_proveedor:
                    servicios_por_proveedor[pid] = {
                        "proveedor": ps.proveedor,
                        "servicios": set()
                    }
                servicios_por_proveedor[pid]["servicios"].add(ps.servicio)

        if not servicios_por_proveedor:
            return Response(status=status.HTTP_204_NO_CONTENT)

        # Convertir sets a listas para el serializer
        datos_serializables = [
            {
                "proveedor": entry["proveedor"],
                "servicios": list(entry["servicios"]),
            }
            for entry in servicios_por_proveedor.values()
        ]

        serializer = BuscarUsuarioSerializer(datos_serializables, many=True)
        return Response(serializer.data)