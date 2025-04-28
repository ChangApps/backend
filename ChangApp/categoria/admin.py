from django.contrib import admin
from ChangApp.categoria.models import Categoria
from ChangApp.servicio.models import Servicio

class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'categoria_padre')
    search_fields = ('nombre',)
    list_filter = ('categoria_padre',)


admin.site.register(Categoria,CategoriaAdmin)