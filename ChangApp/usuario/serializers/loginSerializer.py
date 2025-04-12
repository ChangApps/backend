from django.contrib.auth import authenticate
from rest_framework import serializers

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    
    def validate(self, data):
        usuario = authenticate(username=data['username'], password=data['password'])
        if usuario and usuario.is_active:
            return {'user': usuario}
        raise serializers.ValidationError("Nombre de usuario o contraseña inválidos")
