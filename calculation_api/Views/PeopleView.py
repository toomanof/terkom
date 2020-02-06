from rest_framework.response import Response
from rest_framework.views import APIView

from ..Serializers.PeopleSerializer import PeopleSerializer
from calculation.models.people import People


class PeopleViewSet(APIView):
    def get(self, request):
        queryset = People.objects.all()
        serializer_class = PeopleSerializer(queryset, many=True)
        return Response({"results": serializer_class.data, "pagination": {"more": False}})
