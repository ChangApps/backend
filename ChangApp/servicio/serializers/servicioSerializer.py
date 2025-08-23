from ChangApp.categoria.models import Categoria
from ChangApp.servicio.models.proveedorServicioModels import ProveedorServicio
from rest_framework import serializers
from ChangApp.servicio.models.servicioModels import Servicio, HorarioServicio
from ChangApp.categoria.serializers.categoriaSerializers import CategoriaSerializer

class HorarioServicioSerializer(serializers.ModelSerializer):
    class Meta:
        model = HorarioServicio
        fields = ['dia', 'desdeHora', 'hastaHora']

    def validate(self, data):
        if data['desdeHora'] >= data['hastaHora']:
            raise serializers.ValidationError("La hora de inicio debe ser menor que la hora de fin.")
        return data
    
class ServicioSerializer(serializers.ModelSerializer):
    dias = HorarioServicioSerializer(many=True)
    fechaDesde = serializers.SerializerMethodField()
    
    # Para crear/actualizar: lista de IDs de categorías
    categoria_ids = serializers.PrimaryKeyRelatedField(
        queryset=Categoria.objects.all(),
        source='categorias',  # mapea al ManyToMany
        many=True,
        write_only=True,
        help_text="IDs de las categorías a las que pertenece el servicio"
    )
    
    # Para mostrar en GET: categorías completas
    categorias = CategoriaSerializer(read_only=True, many=True)

    class Meta:
        model = Servicio
        fields = ['id', 'nombreServicio', 'descripcion', 'dias', 'fechaDesde', 'categoria_ids', 'categorias']

    def create(self, validated_data):
        dias_data = validated_data.pop('dias')
        categorias_data = validated_data.pop('categorias', [])
        
        servicio = Servicio.objects.create(**validated_data)
        servicio.categorias.set(categorias_data)
        
        for dia_data in dias_data:
            HorarioServicio.objects.create(servicio=servicio, **dia_data)
        return servicio

    def update(self, instance, validated_data):
        dias_data = validated_data.pop('dias', None)
        categorias_data = validated_data.pop('categorias', None)

        instance.nombreServicio = validated_data.get('nombreServicio', instance.nombreServicio)
        instance.descripcion = validated_data.get('descripcion', instance.descripcion)
        instance.save()

        if categorias_data is not None:
            instance.categorias.set(categorias_data)

        if dias_data is not None:
            instance.dias.all().delete()
            for dia_data in dias_data:
                HorarioServicio.objects.create(servicio=instance, **dia_data)

        return instance

    def get_fechaDesde(self, servicio):
        proveedor = self.context.get('proveedor')
        if proveedor:
            relacion = ProveedorServicio.objects.filter(
                proveedor=proveedor, servicio=servicio
            ).order_by('-fechaDesde').first()
            if relacion:
                return relacion.fechaDesde
        return None