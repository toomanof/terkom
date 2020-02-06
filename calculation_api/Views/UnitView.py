from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ..Serializers.UnitSerializer import UnitSerializer
from calculation.models.unit import Unit


class UnitViewGet(APIView):
    def get(self, request):
        queryset = Unit.objects.all()
        serializer_class = UnitSerializer(queryset, many=True)
        return Response(serializer_class.data)


class UnitSelectGet(APIView):
    def get(self, request):
        if request.GET.get('q'):
            queryset = Unit.objects.filter(short_name__icontains=request.GET.get('q'))
        else:
            queryset = Unit.objects.all()

        elements = []

        for obj in queryset:
            elements.append({'id': obj.id, "text": obj.short_name})

        return Response({"results": elements, "pagination": {"more": False}})
