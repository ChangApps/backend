from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings
from django.core.cache import cache
from random import randint

User = get_user_model()


class EnviarCodigoVerificacionSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def enviarMail(self, validated_data):
        # Primero obtenemos el email
        email = validated_data['email']

        # Verificamos si el email existe en la base de datos
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError({"error": "El correo no está registrado."})

        # Generamos un código de verificación (número aleatorio de 6 dígitos)
        verification_code = randint(100000, 999999)

        # Guardamos el código en caché con la clave basada en el email (expira en 5 minutos)
        cache.set(f"verification_code_{email}", verification_code, timeout=300)

        # Enviamos el código de verificación por correo
        send_mail(
            'Código de verificación',
            f'Hola, tu código de verificación es: {verification_code}',
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
        )

        # Retornamos un mensaje indicando que el código fue enviado
        return {"message": "Código de verificación enviado al correo"}
    

    def enviarMailSinBD(self, validated_data):
        email = validated_data['email']

        # Generamos un código de verificación (número aleatorio de 6 dígitos)
        verification_code = randint(100000, 999999)

        # Guardamos el código en caché con una expiración de 5 minutos
        cache.set(f"verification_code_{email}", verification_code, timeout=300)

        # Enviamos el código de verificación por correo
        send_mail(
            'Código de verificación',
            f'Hola, tu código de verificación es: {verification_code}',
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
        )

        return {"message": "Código de verificación enviado al correo"}

