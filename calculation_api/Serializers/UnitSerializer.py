from rest_framework import serializers
from calculation.models.unit import Unit

class UnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unit
        fields = ['id', 'short_name', 'full_name', 'code']
