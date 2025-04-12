from datetime import date
from ChangApp.usuario.models.usuarioModels import Usuario
from ChangApp.usuario.models.direccionModels import Direccion
from rest_framework import serializers
from .direccionSerializer import DireccionSerializer

class UsuarioSerializer(serializers.ModelSerializer):
    direccion = DireccionSerializer()
    password2 = serializers.CharField(write_only=True, required=False)  # password2 solo se necesita en la creación
    password = serializers.CharField(write_only=True, required=False)   # password es opcional en la actualización
    old_password = serializers.CharField(write_only=True, required=False)  # Para validar contraseña actual
    cantServiciosContratados = serializers.IntegerField(read_only=True)
    cantServiciosTrabajados = serializers.IntegerField(read_only=True)
    puntaje = serializers.FloatField(read_only=True)

    class Meta:
        model = Usuario
        fields = [
            'id', 'username', 'first_name', 'last_name', 'email', 'password', 'old_password','password2', 'documento', 'telefono', 
            'fotoPerfil', 'fechaNacimiento', 'direccion','cantServiciosContratados', 'cantServiciosTrabajados', 'puntaje','bloqueados', 'is_verified'# 'fechaDisponible', 'horarioDisponible'
        ]
        extra_kwargs = {
            'password': {'write_only': True, 'required': False},  # No es obligatorio en la actualización
            'password2': {'write_only': True, 'required': False},  # No es obligatorio en la actualización
            'direccion': {'required': False},
            'fechaNacimiento': {'required': True}
        }

    def validate(self, data):
        if self.instance is None and 'fechaNacimiento' in data:
            birthdate = data['fechaNacimiento']
            today = date.today()
            age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
            
            if age < 18:
                raise serializers.ValidationError({
                    "fechaNacimiento": "Debes tener al menos 18 años para registrarte."
                })

        # Validación para creación de usuario
        if self.instance is None:  # Es una creación
            if 'password' in data and 'password2' in data:
                if data['password'] != data['password2']:
                    raise serializers.ValidationError({"password": "Las contraseñas no coinciden."})
        
        # Validación para cambio de contraseña
        elif 'password' in data:  # Es una actualización y se intenta cambiar la contraseña
            if not 'old_password' in data:
                raise serializers.ValidationError({"old_password": "Debe proporcionar la contraseña actual."})
            
            if not self.instance.check_password(data['old_password']):
                raise serializers.ValidationError({"old_password": "La contraseña actual es incorrecta."})

        email = data.get('email', None)
        username = data.get('username', None)
        telefono = data.get('telefono', None)

        # Validaciones de unicidad excluyendo la instancia actual
        if email and Usuario.objects.exclude(pk=getattr(self.instance, 'pk', None)).filter(email=email).exists():
            raise serializers.ValidationError({"email": "El correo electrónico ya está en uso."})

        if username and Usuario.objects.exclude(pk=getattr(self.instance, 'pk', None)).filter(username=username).exists():
            raise serializers.ValidationError({"username": "El nombre de usuario ya está en uso."})

        if telefono and Usuario.objects.exclude(pk=getattr(self.instance, 'pk', None)).filter(telefono=telefono).exists():
            raise serializers.ValidationError({"telefono": "El número de teléfono ya está en uso."})
        return data
    def create(self, validated_data):
        # Extrae los datos de la contraseña
        validated_data.pop('old_password', None)

        # Extrae los datos de la dirección
        direccion_data = validated_data.pop('direccion')
        
        # Crea una nueva instancia de la dirección
        direccion = Direccion.objects.create(**direccion_data)
    
        # Crea el usuario y asocia la dirección creada
        usuario = Usuario.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
            documento=validated_data['documento'],
            telefono=validated_data['telefono'],
            fechaNacimiento = validated_data.get('fechaNacimiento', None),
            direccion=direccion,
            is_verified=True 
        )
        return usuario
            
    def update(self, instance, validated_data):
        # Maneja la actualización de contraseña si está presente
        if 'password' in validated_data:
            instance.set_password(validated_data.pop('password'))

        # Remueve campos que no queremos actualizar
        validated_data.pop('old_password', None)
        validated_data.pop('password2', None)
        validated_data.pop('fechaNacimiento', None)  # Asegura que no se actualice la fecha de nacimiento
        
        # Maneja la actualización de la dirección
        if 'direccion' in validated_data:
            direccion_data = validated_data.pop('direccion')
            if instance.direccion:
                for key, value in direccion_data.items():
                    setattr(instance.direccion, key, value)
                instance.direccion.save()
            else:
                direccion = Direccion.objects.create(**direccion_data)
                instance.direccion = direccion
        
        # Actualiza los campos restantes
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        instance.save()
        return instance
    
    def update_password_without_old(self, instance, validated_data):
        if 'password' in validated_data:
            instance.set_password(validated_data['password'])
            instance.save()
        return instance

    def obtener_id(self, validated_data):
        email = validated_data['email']
        try:
            usuario = Usuario.objects.get(email=email)
            return {"id": usuario.id}
        except Usuario.DoesNotExist:
            raise serializers.ValidationError({"email": "No se encontró un usuario con este correo electrónico"})

