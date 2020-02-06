from rest_framework import serializers
from calculation.models.dish import Dish


class DishSerializerGet(serializers.ModelSerializer):
    unit = serializers.SerializerMethodField('get_unit')
    tech_map = serializers.SerializerMethodField('get_tech_map')

    def get_unit(self, obj: Dish):
        return {"name": obj.unit.short_name, "id": obj.unit.id} if obj.unit else {"name": '', "id": ''}

    def get_tech_map(self, obj: Dish):
        return {"name": str(obj.tech_map), "id": obj.tech_map.id} if obj.tech_map else {"name": '', "id": ''}

    class Meta:
        model = Dish
        fields = ['id', 'name', 'unit', 'out', 'tech_map']


class DishSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        return Dish.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.unit = validated_data.get('unit', instance.unit)
        instance.out = validated_data.get('out', instance.out)
        instance.tech_map = validated_data.get('tech_map', instance.tech_map)
        instance.save()
        return instance

    class Meta:
        model = Dish
        fields = ['id', 'name', 'unit', 'out', 'tech_map']
