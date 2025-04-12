from rest_framework import serializers
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()

class ObtenerUsernameSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def obtenerYEnviarUsername(self, validated_data):
        email = validated_data['email']

        # Verificamos si el correo existe en la base de datos
        usuario = User.objects.filter(email=email).first()
        if not usuario:
            raise serializers.ValidationError({"email": "No se encontró un usuario con este correo electrónico"})

        username = usuario.username

        # Enviar el nombre de usuario por correo
        send_mail(
            'Recuperación de Nombre de Usuario',
            f'Hola, tu nombre de usuario es: {username}',
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
        )

        return {"message": "El nombre de usuario ha sido enviado a tu correo"}