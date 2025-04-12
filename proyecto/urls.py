
from django.contrib import admin
from django.urls import path, include 
from django.conf.urls.static import static
from django.conf import settings
from ChangApp.views import *
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from ChangApp.views.usuarioViewSet import LoginView, LogoutView
from ChangApp.views.bloqueoUsuarios import BloquearUsuarioView, DesbloquearUsuarioView, UsuariosBloqueadosView
from ChangApp.views.usuarioViewSet import VerificarEmailView,ValidarUsuarioView,ObtenerUsernameView,ValidarCodigoVerificacionView
from ChangApp.views.proveedorServicioViewSet import VerificarProveedorServicio
from ChangApp.views.historialViews import HistorialViewSet
#Swagger
from django.urls import re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

router = routers.DefaultRouter()
router.register(r'usuarios', UsuarioViewSet)
router.register(r'categorias', CategoriaViewSet)
router.register(r'direcciones', DireccionViewSet)
router.register(r'fotos', FotosViewSet)
router.register(r'notificaciones', NotificacionViewSet)
router.register(r'proveedores-servicios', ProveedorServicioViewSet)
router.register(r'servicios', ServicioViewSet)
router.register(r'solicitudes', SolicitudViewSet)

schema_view = get_schema_view(
   openapi.Info(
      title="ChanguitasApp Docs",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
   #  path('', ReactView.as_view(), name="xxx"),
   #  path('', DireccionView.as_view(), name='direccion_view'),
   #  path('usuario/', UsuarioView.as_view(), name='usuario_view') !!!! quizas no va ya que usuarioViewSet seria lo mismo y mejor !!!!,
   #  path('clientes/', ClienteView.as_view(), name='clientes'),
    path('admin/', admin.site.urls),
    path('', include(router.urls), name='api'),
    path('api/token', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/refresh', RefreshView.as_view(), name='refresh'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
#  path('verificar-email/<str:token>/', verificar_email, name='verificar-email'),
    path('verificar-email/', VerificarEmailView.as_view(), name='verificar-email'),
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redocs/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('buscar-proveedores/', BuscarProveedoresAPIView.as_view(), name='buscar_proveedores'),
    path('bloquear/', BloquearUsuarioView.as_view(), name="bloquear_usuario"),
    path('desbloquear/', DesbloquearUsuarioView.as_view(), name="desbloquear_usuario"),
    path('bloqueados/', UsuariosBloqueadosView.as_view(), name="usuarios_bloqueados"),
    path('validar/', ValidarUsuarioView.as_view(), name='validar_usuario'),
    path('validar-codigo/', ValidarCodigoVerificacionView.as_view(), name='validar-codigo'),
    path('obtener-username/', ObtenerUsernameView.as_view(), name='obtener-username'),
    path('proveedores-servicios/usuario/<int:user_id>/', ProveedorServicioViewSet.as_view({'get': 'get_proveedor_servicio_by_user'}), name='proveedor_servicio_by_user'),
    path('proveedores-servicios/usuario/<int:user_id>/<int:servicio_id>/', VerificarProveedorServicio.as_view(), name='verificar_proveedor_servicio'),
    path('historial/<int:usuario_id>/', HistorialViewSet.as_view({'get': 'list'}), name='historial'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
