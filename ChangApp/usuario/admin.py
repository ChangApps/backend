from django.contrib import admin
from ChangApp.usuario.models.direccionModels import Direccion
from ChangApp.usuario.models.usuarioModels import Usuario
from ChangApp.usuario.models.direccionModels import Direccion
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.safestring import mark_safe

@admin.register(Direccion)
class DireccionAdmin(admin.ModelAdmin):
    list_display = ("id", "calle", "altura", "nroDepto", "piso", "barrio")
    search_fields = ("calle", "barrio")

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin): 

    readonly_fields = ['get_fotoPerfil',]   
    ordering = ('last_name',)   
    search_fields = ('first_name',
                     'last_name',
                     'fechaNacimiento',
                     'documento'
                     )  
    list_filter = ('fechaNacimiento', 
                   'is_staff', 
                   'is_superuser', 
                   'is_active'    
                   )
    date_hierarchy='fechaNacimiento'
    list_display = ('get_fotoPerfil',
                    'username',
                    'first_name',
                    'last_name',
                    'is_staff',
                    'is_superuser',
                    'documento',
                    'telefono',
                    'fechaNacimiento',
                    'puntaje',
                    'is_active'
                    ) 
    list_display_links = ('get_fotoPerfil',
                          'first_name',
                          'last_name',
                         )  
    list_per_page = 5   

    # Acciones personalizadas
    actions = ['activar_usuarios', 'desactivar_usuarios']

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Información personal', {'fields': ('first_name', 'last_name', 'direccion', 'documento', 'telefono', 'fechaNacimiento', 'fotoPerfil', 'puntaje')}),
        ('Permisos', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Fechas importantes', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'first_name', 'last_name', 'documento', 'telefono', 'fechaNacimiento', 'fotoPerfil', 'puntaje', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
    )

    def get_fotoPerfil(self, obj):
         if obj.fotoPerfil:
             return mark_safe(f'<img src="{obj.fotoPerfil.url}" width="50" height="50" />')
         return "No hay foto"
    
    get_fotoPerfil.short_description = 'Foto de perfil'