from django.apps import AppConfig

class UsuarioConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ChangApp.usuario'

def ready(self):
    from ChangApp.usuario import models  # ¡Importante para cargar los modelos!