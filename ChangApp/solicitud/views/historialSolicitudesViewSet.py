from rest_framework import viewsets, status
from rest_framework.response import Response
from ChangApp.solicitud.models import Solicitud
from ChangApp.solicitud.serializers.solicitudSerializer import SolicitudSerializer
from ChangApp.usuario.models import Usuario

class HistorialSolicitudesViewSet(viewsets.ViewSet):
    def get_solicitudes_cliente(self, request, *args, **kwargs):
        usuario_id = self.kwargs.get("usuario_id")
        if not usuario_id:
            return Response(
                {"error": "Debe proporcionar un ID de usuario"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            usuario = Usuario.objects.get(id=usuario_id)
        except Usuario.DoesNotExist:
            return Response(
                {"error": "Usuario no encontrado"},
                status=status.HTTP_404_NOT_FOUND
            )

        # Base: todas las solicitudes donde soy cliente
        qs = Solicitud.objects.filter(cliente_id=usuario_id)

       # IDs de usuarios que YO bloqueé
        ids_bloqueados_por_mi = list(usuario.bloqueados.values_list('id', flat=True))

        # IDs de usuarios que ME bloquearon
        ids_que_me_bloquearon = list(Usuario.objects.filter(bloqueados=usuario).values_list('id', flat=True))

        # Filtrar solicitudes excluyendo proveedores bloqueados
        qs = Solicitud.objects.filter(cliente_id=usuario_id)

        # Excluir solicitudes cuyo proveedor está bloqueado por mí
        if ids_bloqueados_por_mi:
            qs = qs.exclude(proveedorServicio__proveedor_id__in=ids_bloqueados_por_mi)

        # Excluir solicitudes cuyo proveedor me bloqueó a mí
        if ids_que_me_bloquearon:
            qs = qs.exclude(proveedorServicio__proveedor_id__in=ids_que_me_bloquearon)

        qs = qs.distinct()

        if not qs.exists():
            return Response(
                {
                    "message": "No se encontraron solicitudes para este usuario donde sea cliente",
                    "data": [],
                },
                status=status.HTTP_200_OK,
            )

        serializer = SolicitudSerializer(qs, many=True)
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