from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from ChangApp.usuario.models.usuarioModels import Usuario
from ChangApp.usuario.serializers.usuarioSerializer import UsuarioSerializer
from ChangApp.usuario.serializers.bloquearUsuarioSerializer import BloquearUsuarioSerializer

class BloquearUsuarioView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = BloquearUsuarioSerializer(data=request.data)
        if serializer.is_valid():
            usuario_a_bloquear_id = serializer.validated_data['usuario_id']
            usuario_actual = request.user

            try:
                usuario_a_bloquear = Usuario.objects.get(id=usuario_a_bloquear_id)
                usuario_actual.bloquear_usuario(usuario_a_bloquear)
                return Response({"message": "Usuario bloqueado con éxito."}, status=status.HTTP_200_OK)
            except Usuario.DoesNotExist:
                return Response({"error": "Usuario no encontrado."}, status=status.HTTP_404_NOT_FOUND)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DesbloquearUsuarioView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = BloquearUsuarioSerializer(data=request.data)
        if serializer.is_valid():
            usuario_a_desbloquear_id = serializer.validated_data['usuario_id']
            usuario_actual = request.user

            try:
                usuario_a_desbloquear = Usuario.objects.get(id=usuario_a_desbloquear_id)
                usuario_actual.desbloquear_usuario(usuario_a_desbloquear)
                return Response({"message": "Usuario desbloqueado con éxito."}, status=status.HTTP_200_OK)
            except Usuario.DoesNotExist:
                return Response({"error": "Usuario no encontrado."}, status=status.HTTP_404_NOT_FOUND)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UsuariosBloqueadosView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        usuario_actual = request.user
        usuarios_bloqueados = usuario_actual.bloqueados.all()
        serializer = UsuarioSerializer(usuarios_bloqueados, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)