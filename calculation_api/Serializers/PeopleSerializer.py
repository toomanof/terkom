from rest_framework import serializers
from calculation.models.people import People


class PeopleSerializer(serializers.ModelSerializer):
    text = serializers.SerializerMethodField('get_fio')

    def get_fio(self, obj: People):
        return str(obj)
    class Meta:
        model = People
        fields = ['id', 'text']
