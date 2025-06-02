from django.apps import AppConfig


class NotificacionConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ChangApp.notificacion'

    def ready(self):
        import ChangApp.notificacion.signalsNotificacionSolicitud