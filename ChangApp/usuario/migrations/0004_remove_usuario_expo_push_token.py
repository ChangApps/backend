# Generated by Django 5.1.2 on 2025-05-05 23:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usuario', '0003_usuario_expo_push_token'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usuario',
            name='expo_push_token',
        ),
    ]
