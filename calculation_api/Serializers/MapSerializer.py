from rest_framework import serializers
from calculation.models.map import Map, MapItems


class MapFullSerializerGet(serializers.ModelSerializer):
    approved = serializers.SerializerMethodField('get_approved')
    agreed = serializers.SerializerMethodField('get_agreed')
    unit = serializers.SerializerMethodField('get_unit')
    items = serializers.SerializerMethodField('get_items')

    def get_approved(self, obj: Map):
        return {"id": obj.approved.id, "text": str(obj.approved)}

    def get_approved(self, obj: Map):
        return {"id": obj.unit.id, "text": str(obj.approved)}

    def get_agreed(self, obj: Map):
        return {"id": obj.agreed.id, "text": str(obj.agreed)}

    def get_unit(self, obj: Map):
        return {"id": obj.unit.id, "text": obj.unit.short_name}

    def get_items(self, obj: Map):
        items = MapItems.objects.filter(map_doc=obj)
        returned_value = []
        for item in items:
            returned_value.append(
                {"id": item.id, "position": item.position,
                 "product": {"id": item.product.id, "text": item.product.name}, "brutto": str(item.brutto),
                 "netto": str(item.netto)})
        return returned_value

    class Meta:
        model = Map
        fields = ['id', 'name', 'source', 'approved', 'agreed', 'technology', 'created_at', 'batch_output', 'unit',
                  'items']


class MapSerializerGet(serializers.ModelSerializer):
    # approved = serializers.StringRelatedField(many=False)
    # agreed = serializers.StringRelatedField(many=False)
    unit = serializers.StringRelatedField(many=False)

    class Meta:
        model = Map
        fields = ['id', 'name', 'source', 'batch_output', 'unit']


class MapSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        return Map.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.source = validated_data.get('source', instance.source)
        instance.approved = validated_data.get('approved', instance.approved)
        instance.agreed = validated_data.get('agreed', instance.agreed)
        instance.technology = validated_data.get('technology', instance.technology)
        instance.batch_output = validated_data.get('batch_output', instance.batch_output)
        instance.unit = validated_data.get('unit', instance.unit)
        instance.save()
        return instance

    class Meta:
        model = Map
        fields = ['id', 'name', 'source', 'approved', 'agreed', 'technology', 'batch_output', 'unit']


class MapItemsSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        return MapItems.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.map_doc = validated_data.get('map_doc', instance.map_doc)
        instance.position = validated_data.get('position', instance.position)
        instance.product = validated_data.get('product', instance.product)
        instance.brutto = validated_data.get('brutto', instance.brutto)
        instance.netto = validated_data.get('netto', instance.netto)
        instance.save()
        return instance

    class Meta:
        model = MapItems
        fields = ['id', 'map_doc', 'position', 'product', 'brutto', 'netto']
