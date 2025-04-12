from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ChangApp.usuario.models.usuarioModels import Usuario

class ObtenerIdPorEmailView(APIView):
    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response({"detail": "El correo electrónico es obligatorio."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            usuario = Usuario.objects.get(email=email)
            return Response({"id": usuario.id}, status=status.HTTP_200_OK)
        except Usuario.DoesNotExist:
            return Response({"detail": "No se encontró un usuario con este correo electrónico."}, status=status.HTTP_404_NOT_FOUND)