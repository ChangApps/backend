from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from ChangApp.usuario.serializers.enviarCodigoVerificacionSerializer import EnviarCodigoVerificacionSerializer
from drf_yasg.utils import swagger_auto_schema

class VerificarEmailView(APIView):
    @swagger_auto_schema(request_body=EnviarCodigoVerificacionSerializer)
    def post(self, request, *args, **kwargs):
        # Si la URL es 'verificar-email', se ejecuta esta lógica
        if self.request.path == '/verificar-email/':
            # Lógica para verificar el email (con base de datos)
            serializer = EnviarCodigoVerificacionSerializer(data=request.data)
            if serializer.is_valid():
                response = serializer.enviarMail(serializer.validated_data)
                return Response(response, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        # Si la URL es 'enviar-email', se ejecuta esta lógica
        elif self.request.path == '/enviar-email/':
            # Lógica para enviar el email sin verificación en la base de datos
            serializer = EnviarCodigoVerificacionSerializer(data=request.data)
            if serializer.is_valid():
                response = serializer.enviarMailSinBD(serializer.validated_data)
                return Response(response, status=status.HTTP_200_OK)
<<<<<<< HEAD
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
=======
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
>>>>>>> 0fa66f4f29e6180f54916608f0218a6597cd8adb
