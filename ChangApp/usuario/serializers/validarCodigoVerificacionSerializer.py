from rest_framework import serializers
from django.core.cache import cache

class ValidarCodigoVerificacionSerializer(serializers.Serializer):
    email = serializers.EmailField()  
    codigo = serializers.IntegerField()

    def validate(self, validated_data):
        # Obtenemos el código ingresado y el email
        codigo_ingresado = validated_data["codigo"]
        email = validated_data["email"]

        # Obtenemos el código almacenado en caché utilizando el email
        codigo_guardado = cache.get(f"verification_code_{email}")

        if codigo_guardado is None:
            raise serializers.ValidationError({"codigo": "El código ha expirado o no existe."})

        if codigo_guardado != codigo_ingresado:
            raise serializers.ValidationError({"codigo": "El código ingresado es incorrecto."})

        # Si el código es válido, eliminarlo de la caché para que no pueda reutilizarse
        cache.delete(f"verification_code_{email}")

        return validated_data

