from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from ChangApp.usuario.serializers.usuarioSerializer import UsuarioSerializer

class ValidarUsuarioView(APIView):
    def post(self, request, *args, **kwargs):
        # Recibimos los datos del usuario
        serializer = UsuarioSerializer(data=request.data)
        
        # Validamos los datos
        if serializer.is_valid():
            return Response({"message": "Los datos son válidos."}, status=status.HTTP_200_OK)
        
        # Si hay errores de validación, los devolvemos
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)