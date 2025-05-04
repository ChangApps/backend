from django.contrib import admin
from ChangApp.notificacion.models import Notificacion

@admin.register(Notificacion)
class NotificacionAdmin(admin.ModelAdmin):
    list_display = ('usuario_destino', 'mensaje_resumido', 'notificacion_de_sistema', 'fechahora_creada')
    list_filter = ('notificacion_de_sistema', 'fechahora_creada')
    search_fields = ('usuario_destino__username', 'mensaje')

    def mensaje_resumido(self, obj):
        return obj.mensaje[:50]
    mensaje_resumido.short_description = 'Mensaje'
