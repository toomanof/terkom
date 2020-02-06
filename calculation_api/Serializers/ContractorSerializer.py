from rest_framework import serializers
from calculation.models.contractor import Contractor


class ContractorSerializer(serializers.ModelSerializer):
    abs_url = serializers.SerializerMethodField('get_absolute_url')

    def get_absolute_url(self, obj: Contractor):
        return obj.get_absolute_url()

    class Meta:
        model = Contractor
        fields = ['id', 'name', 'type_c', 'abs_url']
