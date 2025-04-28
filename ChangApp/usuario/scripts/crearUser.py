from ChangApp.usuario.models.usuarioModels import Usuario
from ChangApp.usuario.models.direccionModels import Direccion

def run():
    direccion = Direccion.objects.create(
        calle='Av. Siempreviva',
        altura=742,
        nroDepto=5,
        piso=2,
        barrio='Centro'
    )

    usuario = Usuario.objects.create_user(
        username='majo',
        password='Majo123',
        first_name='Majo',
        last_name='Flores',
        email='majo@example.com',
        documento='12345678',
        telefono='1234567890',
        fechaNacimiento='2002-04-06',
        direccion=direccion,
        is_verified=True
    )

    print("✅ Usuario creado:", usuario)
