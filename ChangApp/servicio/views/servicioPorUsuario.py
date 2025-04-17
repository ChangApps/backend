from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from ChangApp.servicio.models.proveedorServicioModels import ProveedorServicio
from ChangApp.servicio.serializers.servicioSerializer import ServicioSerializer
from ChangApp.usuario.models.usuarioModels import Usuario

# Mixin es una clase que tiene métodos que querés “mezclar” dentro de otra clase principal.
class ServicioPorUsuarioMixin:
    #Para traer los servicios que tiene vinculado un usuario
    @action(detail=False, methods=['get'], url_path='por-usuario/(?P<usuario_id>[^/.]+)')
    def por_usuario(self, request, usuario_id=None):
        try:
            # Busca el usuario
            usuario = Usuario.objects.get(id=usuario_id)

            # Obtiene los servicios asociados al usuario
            proveedor_servicios = ProveedorServicio.objects.filter(proveedor=usuario)
            
            # Obtenga servicios únicos para evitar duplicados
            servicios = list({ps.servicio.id: ps.servicio for ps in proveedor_servicios}.values())

            # Serializa los servicios
            serializer = ServicioSerializer(servicios, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Usuario.DoesNotExist:
            return Response({'error': 'Usuario no encontrado'}, status=status.HTTP_404_NOT_FOUND)

#Le pongo Mixin porque es una convención muy usada en Django y DRF para indicar 
# que esa clase no es una vista completa, sino una pieza reutilizable que agrega 
# una funcionalidad específica a otra clase (como un ViewSet).