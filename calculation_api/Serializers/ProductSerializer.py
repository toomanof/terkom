from rest_framework import serializers
from calculation.models.product import Product


class ProductSerializerForSelect(serializers.ModelSerializer):
    text = serializers.SerializerMethodField('name_to_text')

    def name_to_text(self, obj: Product):
        return obj.name

    class Meta:
        model = Product
        fields = ['id', 'text']


class ProductSerializerGet(serializers.ModelSerializer):
    unit = serializers.SerializerMethodField('get_unit')
    dish = serializers.SerializerMethodField('get_dish')
    abs_url = serializers.SerializerMethodField('get_absolute_url')

    def get_unit(self, obj: Product):
        return {"name": obj.unit.short_name, "id": obj.unit.id} if obj.unit else {"name": '', "id": ''}

    def get_dish(self, obj: Product):
        return {"name": obj.dish.name, "id": obj.dish.id} if obj.dish else {"name": '', "id": ''}

    def get_absolute_url(self, obj: Product):
        return obj.get_absolute_url()

    class Meta:
        model = Product
        fields = ['id', 'name', 'unit', 'dish', 'weight', 'abs_url']


class ProductSerializerSet(serializers.ModelSerializer):
    def create(self, validated_data):
        return Product.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.unit = validated_data.get('unit', instance.unit)
        instance.dish = validated_data.get('dish', instance.dish)
        instance.weight = validated_data.get('weight', instance.weight)
        instance.save()
        return instance

    class Meta:
        model = Product
        fields = ['id', 'name', 'unit', 'dish', 'weight']
