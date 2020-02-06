from rest_framework import serializers
from calculation.models.calculation import Calculation


class CalculationSerializer(serializers.ModelSerializer):
    def create(self, validated_data: dict):
        return Calculation.objects.create(**validated_data)

    def update(self, instance: Calculation, validated_data: dict):
        instance.qty_children = validated_data.get('qty_children', instance.qty_children)
        instance.dish = validated_data.get('dish', instance.dish)
        instance.created_at = validated_data.get('created_at', instance.created_at)
        instance.set_number_of_food_products()
        instance.food_intake = validated_data.get('food_intake', instance.food_intake)
        instance.save()
        return instance

    class Meta:
        model = Calculation
        fields = ['id', 'qty_children', 'dish', 'created_at', 'values', 'food_intake']
