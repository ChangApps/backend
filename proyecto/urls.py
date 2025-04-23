
from django.contrib import admin
from django.urls import path, include 
from django.conf.urls.static import static
from django.conf import settings

#Views
from ChangApp.categoria.views.categoriaViewSet import CategoriaViewSet
from ChangApp.usuario.views import UsuarioViewSet, VerificarEmailView, ActualizarContrasenaView, DireccionViewSet, FotosViewSet, LoginView, LogoutView, RefreshView, ObtenerIdPorEmailView, ObtenerUsernameView, ValidarCodigoVerificacionView, ValidarUsuarioView, UsuariosBloqueadosView, BloquearUsuarioView, DesbloquearUsuarioView
from ChangApp.notificacion.views import NotificacionViewSet
from ChangApp.servicio.views import BuscarProveedoresAPIView, ProveedorServicioPorUsuarioView, ProveedorServicioViewSet, ServicioViewSet, VerificarProveedorServicioView
from ChangApp.solicitud.views import SolicitudViewSet, HistorialSolicitudesViewSet

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework import routers

#Swagger
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
    path('admin/', admin.site.urls),
    path('', include(router.urls), name='api'),
    path('api/token/', TokenObtainPairView.as_view(), name='token-obtain-pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/refresh/', RefreshView.as_view(), name='refresh'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('actualizar-contrasena/', ActualizarContrasenaView.as_view(), name='actualizar-contraseña'),
    path('verificar-email/', VerificarEmailView.as_view(), name='verificar-email'),
    path('enviar-email/',  VerificarEmailView.as_view(), name='enviar-email'),
    path('obtener-id-por-email/', ObtenerIdPorEmailView.as_view(), name="obtener-id-por-email"),
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redocs/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('bloquear/', BloquearUsuarioView.as_view(), name="bloquear-usuario"),
    path('desbloquear/', DesbloquearUsuarioView.as_view(), name="desbloquear-usuario"),
    path('bloqueados/', UsuariosBloqueadosView.as_view(), name="usuarios-bloqueados"),
    path('validar/', ValidarUsuarioView.as_view(), name='validar-usuario'),
    path('validar-codigo/', ValidarCodigoVerificacionView.as_view(), name='validar-codigo'),
    path('obtener-username/', ObtenerUsernameView.as_view(), name='obtener-username'),
    path('proveedor-servicio-por-usuario/usuario/<int:user_id>/', ProveedorServicioPorUsuarioView.as_view({'get': 'get_proveedor_servicio_by_user'}), name='proveedor-servicio-by-user'),
    path('buscar-proveedores/', BuscarProveedoresAPIView.as_view(), name='buscar-proveedores'),
    path('proveedores-servicios/usuario/<int:user_id>/<int:servicio_id>/', VerificarProveedorServicioView.as_view(), name='verificar-proveedor-servicio'),
    path('historial/<int:usuario_id>/', HistorialSolicitudesViewSet.as_view({'get': 'list'}), name='historial'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
