from rest_framework import viewsets
from ChangApp.servicio.models.servicioModels import Servicio
from ChangApp.servicio.serializers.servicioSerializer import ServicioSerializer
from .servicioCreate import ServicioCreateMixin
from .servicioUpdate import ServicioUpdateMixin
from .servicioDestroy import ServicioDestroyMixin
from .servicioPorUsuario import ServicioPorUsuarioMixin

class ServicioViewSet(
    ServicioCreateMixin,
    ServicioUpdateMixin,
    ServicioDestroyMixin,
    ServicioPorUsuarioMixin,
    viewsets.ModelViewSet
):
    queryset = Servicio.objects.all()
    serializer_class = ServicioSerializer
