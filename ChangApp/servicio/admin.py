from django.contrib import admin
from ChangApp.servicio.models.proveedorServicioModels import ProveedorServicio
from ChangApp.servicio.models.servicioModels import Servicio

@admin.register(ProveedorServicio)
class ProveedorServicioAdmin(admin.ModelAdmin):
    list_display = ('servicio', 'proveedor', 'fechaDesde', 'fechaHasta')
    list_filter = ('servicio', 'fechaDesde')
    search_fields = ('proveedor__username', 'servicio__nombreServicio')
    date_hierarchy = 'fechaDesde'

@admin.register(Servicio)
class ServicioAdmin(admin.ModelAdmin):
    list_display = ('nombreServicio', 'dia', 'desdeHora', 'hastaHora')
    list_filter = ('dia',)
    search_fields = ('nombreServicio', 'descripcion')