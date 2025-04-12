from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.crypto import get_random_string
from ChangApp.usuario.models.direccionModels import Direccion
from ChangApp.solicitud.models  import EstadoServicio, Solicitud

# Manager personalizado
class UsuarioManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('El email es obligatorio')
        if not username:
            raise ValueError('El nombre de usuario es obligatorio')

        # Validar campos obligatorios solo para usuarios normales (no superusuarios)
        if not extra_fields.get('is_superuser', False):
            if 'documento' not in extra_fields or not extra_fields['documento']:
                raise ValueError("El campo 'documento' es obligatorio.")
            if 'direccion' not in extra_fields or not extra_fields['direccion']:
                raise ValueError("El campo 'direccion' es obligatorio.")

        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        # Crear el superusuario y omitir la validación de campos obligatorios.
        return self.create_user(username, email, password, **extra_fields)
    
class Usuario(AbstractUser):
    #nombre, apellido, contraseña y email lo trae por defecto el usuario de django
    documento = models.IntegerField(unique=True, blank=False, null=False)
    telefono = models.IntegerField(blank=True, null=False, default=1234)
    # fotoPerfil - blank=True se debe sacar una vez terminado el proyecto
    fotoPerfil = models.ImageField(upload_to='imagenesUsuario', null=True, blank=True, default='imagenesUsuario/empty.jpg')
    fechaNacimiento = models.DateField(blank=False, null=False, verbose_name="fecha nacimiento", default="2000-01-01")
    direccion = models.OneToOneField(Direccion, on_delete=models.CASCADE, null=False)
    # explote las clases hijas Cliente y Proveedor en Usuario ya que un usuario va a poder contratar y ser contratado
    # por lo tanto y al final de cuentas, hace lo mismo sin importar la diferenciación de tipo de usuario.
    fechaDisponible = models.DateField(blank=True, null=True)
    horarioDisponible = models.TimeField(blank=True, null=True)
    #atributos a mostrar en perfil
    cantServiciosContratados = models.IntegerField(blank=True, null=True)
    cantServiciosTrabajados = models.IntegerField(blank=True, null=True)
    puntaje = models.IntegerField(blank=True, null=True)
    
    is_verified = models.BooleanField(default=False)
    verification_token = models.CharField(max_length=64, blank=True, null=True)

    def generate_verification_token(self):
        """Genera un token aleatorio para la verificación del email"""
        self.verification_token = get_random_string(64)
        self.save()

    objects = UsuarioManager()

    bloqueados = models.ManyToManyField("self", symmetrical=False, blank=True)

    def bloquear_usuario(self, usuario):
        """ Bloquea a un usuario """
        self.bloqueados.add(usuario)
        self.save()

    def desbloquear_usuario(self, usuario):
        """ Desbloquea a un usuario """
        self.bloqueados.remove(usuario)
        self.save()
    
    def esta_bloqueado_por(self, usuario):
        """ Retorna True si este usuario está bloqueado por otro usuario """
        return self in usuario.bloqueados.all()
    
    def ha_bloqueado(self, usuario):
        """ Retorna True si este usuario ha bloqueado a otro usuario """
        return usuario in self.bloqueados.all()

    def __str__(self):
        return f"{self.username} ({self.id})"     
             
    def getServiciosContratados(self):
      # Esto asegura que se devuelva un queryset, no una lista de objetos
        return self.solicitudes_cliente.all()
    
    def getServiciosTrabajados(self):
        # Obtiene todas las solicitudes relacionadas con los servicios ofrecidos por el proveedor
        servicios_ofrecidos = self.servicios_ofrecidos.all()  # Relación del proveedor con ProveedorServicio
        solicitudes = Solicitud.objects.filter(proveedorServicio__in=servicios_ofrecidos)
        return solicitudes

    def calcularCantServiciosContratados(self):
        servicios_contratados = self.getServiciosContratados().exclude(estado=EstadoServicio.CANCELADO)
        self.cantServiciosContratados = servicios_contratados.count()
        self.save()  # Este save() es importante para que los cambios persistan

    def calcularCantServiciosTrabajados(self):
        solicitudes_finalizadas = self.getServiciosTrabajados().filter(estado=EstadoServicio.FINALIZADO)
        self.cantServiciosTrabajados = solicitudes_finalizadas.count()
        # Guarda el resultado en la base de datos
        self.save()

    def calcularPuntaje(self):
        solicitudes_finalizadas = self.getServiciosTrabajados().filter(estado=EstadoServicio.FINALIZADO)
        # Calcula el puntaje promedio
        total_valoraciones = solicitudes_finalizadas.aggregate(total=models.Sum('valoracion'))['total'] or 0
        cantidad_finalizadas = solicitudes_finalizadas.count()
        # Evita la división por cero
        self.puntaje = total_valoraciones / cantidad_finalizadas if cantidad_finalizadas > 0 else 0
        # Guarda el resultado en la base de datos
        self.save()
