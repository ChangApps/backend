from django.contrib import admin
from ChangApp.solicitud.models import Solicitud

@admin.register(Solicitud)
class SolicitudAdmin(admin.ModelAdmin):
    list_display = (
        'cliente', 'get_proveedor', 'fechaTrabajo', 'estado', 'valoracion'
    )
    list_filter = ('estado', 'fechaTrabajo')
    search_fields = ('cliente__username', 'proveedorServicio__proveedor__username')
    date_hierarchy = 'fechaTrabajo'

    def get_proveedor(self, obj):
        return obj.proveedorServicio.proveedor.username
    get_proveedor.short_description = 'Proveedor'
