from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from ChangApp.usuario.serializers.obtenerUsernameSerializer import ObtenerUsernameSerializer

class ObtenerUsernameView(APIView):
    def post(self, request):
        serializer = ObtenerUsernameSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.obtenerYEnviarUsername(serializer.validated_data), status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)