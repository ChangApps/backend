from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from ChangApp.usuario.serializers.validarCodigoVerificacionSerializer import ValidarCodigoVerificacionSerializer

class ValidarCodigoVerificacionView(APIView):
    def post(self, request):
        # Crear la instancia del serializer con los datos de la solicitud
        serializer = ValidarCodigoVerificacionSerializer(data=request.data)

        if serializer.is_valid():
            # No es necesario llamar a validar_codigo explícitamente,
            # porque la validación se maneja dentro del método `validate` del serializer
            return Response({"message": "El código de verificación es válido"}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)