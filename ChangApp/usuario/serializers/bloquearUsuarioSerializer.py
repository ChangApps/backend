from rest_framework import serializers

class BloquearUsuarioSerializer(serializers.Serializer):
    usuario_id = serializers.IntegerField()
