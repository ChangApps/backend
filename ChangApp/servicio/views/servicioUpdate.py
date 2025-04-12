from rest_framework import status
from rest_framework.response import Response

# Mixin es una clase que tiene métodos que querés “mezclar” dentro de otra clase principal.
class ServicioUpdateMixin:
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            self.perform_update(serializer)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#Le pongo Mixin porque es una convención muy usada en Django y DRF para indicar 
# que esa clase no es una vista completa, sino una pieza reutilizable que agrega 
# una funcionalidad específica a otra clase (como un ViewSet).