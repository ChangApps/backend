from rest_framework import serializers
from ..models import Usuario

class FCMTokensSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['fcm_token']