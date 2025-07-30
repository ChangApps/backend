from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings
from django.core.cache import cache
from random import randint

User = get_user_model()


class EnviarCodigoVerificacionSerializer(serializers.Serializer):
    email = serializers.EmailField()
    contexto = serializers.ChoiceField(choices=["registro", "recuperacion"])

    def enviarMail(self, validated_data):
        # Primero obtenemos el email
        email = validated_data['email']
        contexto = validated_data['contexto']

        # Verificamos si el email existe en la base de datos
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError({"error": "El correo no está registrado."})

        # Generamos un código de verificación (número aleatorio de 6 dígitos)
        verification_code = randint(100000, 999999)

        # Guardamos el código en caché con la clave basada en el email (expira en 5 minutos)
        cache.set(f"verification_code_{email}", verification_code, timeout=300)

        # Elegir el cuerpo del mensaje según el contexto
        if contexto == "registro":
            subject = "Confirmación de registro - ChangApp"
            message = (
                f"Hola,\n\n"
                f"Gracias por registrarte en ChangApp. Para completar tu registro, por favor ingresá el siguiente código de verificación:\n\n"
                f"🔐 Código:\n\n"
                f"{verification_code}\n\n"
                f"Este código es válido por 5 minutos.\n\n"
                f"Si no solicitaste este registro, podés ignorar este mensaje.\n\n"
                f"Saludos,\n"
                f"El equipo de Changuitas"
            )
        else:  # recuperación
            subject = "Recuperación de contraseña - ChangApp"
            message = (
                f"Hola,\n\n"
                f"Recibimos una solicitud para restablecer tu contraseña en ChangApp.\n\n"
                f"🔐 Tu código de recuperación es:\n\n"
                f"{verification_code}\n\n"
                f"Este código es válido por 5 minutos.\n\n"
                f"Si no solicitaste este cambio, podés ignorar este mensaje.\n\n"
                f"Saludos,\n"
                f"El equipo de Changuitas"
            )

        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
        )

        return {"message": "Código de verificación enviado al correo"}
    

    def enviarMailSinBD(self, validated_data):
        email = validated_data['email']
        contexto = validated_data['contexto']
        
        # Generamos un código de verificación (número aleatorio de 6 dígitos)
        verification_code = randint(100000, 999999)

        # Guardamos el código en caché con una expiración de 5 minutos
        cache.set(f"verification_code_{email}", verification_code, timeout=300)

        # Elegir el cuerpo del mensaje según el contexto
        if contexto == "registro":
            subject = "Confirmación de registro - ChangApp"
            message = (
                f"Hola,\n\n"
                f"Gracias por registrarte en ChangApp. Para completar tu registro, por favor ingresá el siguiente código de verificación:\n\n"
                f"🔐 Código:\n\n"
                f"{verification_code}\n\n"
                f"Este código es válido por 5 minutos.\n\n"
                f"Si no solicitaste este registro, podés ignorar este mensaje.\n\n"
                f"Saludos,\n"
                f"El equipo de Changuitas"
            )
        else:  # recuperación
            subject = "Recuperación de contraseña - ChangApp"
            message = (
                f"Hola,\n\n"
                f"Recibimos una solicitud para restablecer tu contraseña en ChangApp.\n\n"
                f"🔐 Tu código de recuperación es:\n\n"
                f"{verification_code}\n\n"
                f"Este código es válido por 5 minutos.\n\n"
                f"Si no solicitaste este cambio, podés ignorar este mensaje.\n\n"
                f"Saludos,\n"
                f"El equipo de Changuitas"
            )

        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
        )

        return {"message": "Código de verificación enviado al correo"}

