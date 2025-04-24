from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ChangApp.usuario.models.usuarioModels import Usuario
from ChangApp.usuario.serializers.usuarioSerializer import UsuarioSerializer
        
class ActualizarContrasenaView(APIView):
    def patch(self, request):
        user_id = request.data.get("id")
        new_password = request.data.get("password")

        if not user_id or not new_password:
            return Response({"error": "Debe proporcionar el ID del usuario y una nueva contraseña."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            usuario = Usuario.objects.get(id=user_id)
            serializer = UsuarioSerializer()
            serializer.update_password_without_old(usuario, {'password': new_password})
            return Response({"message": "Contraseña actualizada correctamente."}, status=status.HTTP_200_OK)
        except Usuario.DoesNotExist:
            return Response({"error": "Usuario no encontrado."}, status=status.HTTP_404_NOT_FOUND)

