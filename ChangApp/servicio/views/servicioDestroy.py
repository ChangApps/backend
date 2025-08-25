from ChangApp.solicitud.models import EstadoServicio
from rest_framework import status
from rest_framework.response import Response

# Mixin es una clase que tiene métodos que querés “mezclar” dentro de otra clase principal.
class ServicioDestroyMixin:
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()  # Obtiene el servicio a eliminar

        # Verificar si existen solicitudes asociadas en estado PENDIENTE_ACEPTACION o INICIADO
        solicitudes_activas = instance.proveedores_servicio.filter(
            solicitudes__estado__in=[EstadoServicio.PENDIENTE_ACEPTACION, EstadoServicio.INICIADO]
        ).exists()

        if solicitudes_activas:
            return Response(
                {"error": "No se puede eliminar el servicio porque tiene solicitudes pendientes o en curso."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Si no hay solicitudes en esos estados, eliminar
        self.perform_destroy(instance)
        return Response(
            {"message": "Servicio eliminado correctamente."},
            status=status.HTTP_200_OK
        )