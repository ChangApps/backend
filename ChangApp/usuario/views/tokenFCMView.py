from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from ..serializers.tokenFCMSerializer import FCMTokensSerializer

class GuardarFCMTokenView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        usuario = request.user
        serializer = FCMTokensSerializer(usuario, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"detail": "FCM token guardado correctamente"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)