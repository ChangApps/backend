from rest_framework import serializers
from ..models import Usuario

class ExpoPushTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['expo_push_token']