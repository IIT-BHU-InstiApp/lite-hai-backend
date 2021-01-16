from rest_framework import serializers
from .models import ConfigVar

class ConfigVarSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConfigVar
        fields = ('name', 'value')
