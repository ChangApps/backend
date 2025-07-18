# Generated by Django 5.1.2 on 2025-04-30 15:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('usuario', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='direccion',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='usuario.direccion'),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='documento',
            field=models.IntegerField(blank=True, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='Grupos a los que pertenece este usuario.', related_name='usuario_set', to='auth.group', verbose_name='grupos'),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Permisos específicos para este usuario.', related_name='usuario_permissions_set', to='auth.permission', verbose_name='permisos de usuario'),
        ),
    ]
