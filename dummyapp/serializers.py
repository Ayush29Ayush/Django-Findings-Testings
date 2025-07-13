from rest_framework import serializers
from .models import DummyModel

class DummyModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = DummyModel
        fields = ['id', 'num1', 'num2', 'sum']
        read_only_fields = ['id', 'sum']
