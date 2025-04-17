from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from ChangApp.usuario.serializers.enviarCodigoVerificacionSerializer import EnviarCodigoVerificacionSerializer
from drf_yasg.utils import swagger_auto_schema

class VerificarEmailView(APIView):
    @swagger_auto_schema(request_body=EnviarCodigoVerificacionSerializer)
    def post(self, request, *args, **kwargs):
        # Inicializamos el serializer con los datos del request
        serializer = EnviarCodigoVerificacionSerializer(data=request.data)

        # Validar los datos
        if serializer.is_valid():
            # Llamar a la función que enviará el código de verificación
            response = serializer.enviarMail(serializer.validated_data)
            return Response(response, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
