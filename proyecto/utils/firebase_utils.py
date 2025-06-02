import os
import firebase_admin
from firebase_admin import credentials, messaging

firebase_path = os.path.join(os.path.dirname(__file__), '..', 'firebase', 'firebase-config.json')

if not firebase_admin._apps:
    cred = credentials.Certificate(firebase_path)
    firebase_admin.initialize_app(cred)

def enviar_notificacion_push(token, titulo, cuerpo):
    mensaje = messaging.Message(
        notification=messaging.Notification(
            title=titulo,
            body=cuerpo,
        ),
        token=token,
    )
    response = messaging.send(mensaje)
    return response
