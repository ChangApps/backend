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
    list_display = ('nombreServicio', 'mostrar_dias_y_horarios')
    search_fields = ('nombreServicio', 'descripcion')

    def mostrar_dias_y_horarios(self, obj):
        # obj.dias es el related_name del modelo HorarioServicio
        horarios = obj.dias.all()
        return ", ".join([f"{h.dia} {h.desdeHora.strftime('%H:%M')} - {h.hastaHora.strftime('%H:%M')}" for h in horarios])
        mostrar_dias_y_horarios.short_description = 'Días y Horarios'