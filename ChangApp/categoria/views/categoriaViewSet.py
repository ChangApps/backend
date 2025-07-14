from rest_framework import status
from ChangApp.categoria.models import Categoria
from rest_framework.response import Response
from rest_framework import viewsets
from ChangApp.categoria.serializers.categoriaSerializers import CategoriaSerializer
from rest_framework.decorators import action

class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # Guarda la nueva Categoria en la base de datos
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['get'], url_path='subcategorias')
    def obtener_subcategorias(self, request, pk=None):
        subcategorias = Categoria.objects.filter(categoria_padre_id=pk)
        serializer = self.get_serializer(subcategorias, many=True)
        return Response(serializer.data)