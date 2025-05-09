# Generated by Django 5.1.2 on 2025-04-17 01:14

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('categoria', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Servicio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombreServicio', models.CharField(max_length=100)),
                ('descripcion', models.TextField()),
                ('dia', models.CharField(choices=[('Lunes', 'Lun'), ('Martes', 'Mar'), ('Miércoles', 'Mie'), ('Jueves', 'Jue'), ('Viernes', 'Vie'), ('Sábado', 'Sab'), ('Domingo', 'Dom')], default='Lunes', max_length=10)),
                ('desdeHora', models.TimeField(default='00:00')),
                ('hastaHora', models.TimeField(default='00:00')),
                ('categorias', models.ManyToManyField(related_name='servicios', to='categoria.categoria')),
            ],
        ),
        migrations.CreateModel(
            name='ProveedorServicio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fechaDesde', models.DateField()),
                ('fechaHasta', models.DateField(blank=True, null=True)),
                ('proveedor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='servicios_ofrecidos', to=settings.AUTH_USER_MODEL)),
                ('servicio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='proveedores_servicio', to='servicio.servicio')),
            ],
        ),
    ]
