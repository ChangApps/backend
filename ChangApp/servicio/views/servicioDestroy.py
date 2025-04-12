from rest_framework import status
from rest_framework.response import Response

# Mixin es una clase que tiene métodos que querés “mezclar” dentro de otra clase principal.
class ServicioDestroyMixin:
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object() # Obtiene el servicio a eliminar
        self.perform_destroy(instance) # Elimina el servicio de la base de datos
        return Response({"message": "Servicio eliminado correctamente."}, status=status.HTTP_200_OK)

#Le pongo Mixin porque es una convención muy usada en Django y DRF para indicar 
# que esa clase no es una vista completa, sino una pieza reutilizable que agrega 
# una funcionalidad específica a otra clase (como un ViewSet).