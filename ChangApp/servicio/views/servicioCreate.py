from rest_framework import status
from rest_framework.response import Response

# Mixin es una clase que tiene métodos que querés “mezclar” dentro de otra clase principal.
class ServicioCreateMixin:
    def create(self, request, *args, **kwargs):
        # manejo para múltiples registros
        if isinstance(request.data, list):
            serializer = self.get_serializer(data=request.data, many=True)
            if serializer.is_valid():
                self.perform_create(serializer)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            # Manejo para un único registro
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                self.perform_create(serializer)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
#Le pongo Mixin porque es una convención muy usada en Django y DRF para indicar 
# que esa clase no es una vista completa, sino una pieza reutilizable que agrega 
# una funcionalidad específica a otra clase (como un ViewSet).