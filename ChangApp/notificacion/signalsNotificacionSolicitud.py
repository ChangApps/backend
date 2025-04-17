from django.db.models.signals import post_save
from django.dispatch import receiver
from ChangApp.notificacion.models import Notificacion
from ChangApp.solicitud.models import Solicitud

@receiver(post_save, sender=Solicitud)
def crear_notificacion_solicitud(sender, instance, created, **kwargs):
    if created:
        mensaje = f"Se ha creado una nueva solicitud para el proveedor {instance.proveedorServicio.proveedor.username}."
        Notificacion.objects.create(
        Usuario=instance.proveedorServicio.proveedor,  # Usuario que recibe la notificación
        mensaje=mensaje,
        tipoSistema=True
      #  tipoSistema='Solicitud'
    )