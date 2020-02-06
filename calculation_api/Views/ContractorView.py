from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ..Serializers.ContractorSerializer import ContractorSerializer
from calculation.models.contractor import Contractor


class ContractorViewGet(APIView):
    def get(self, request):
        queryset = Contractor.objects.all()
        serializer_class = ContractorSerializer(queryset, many=True)
        return Response(serializer_class.data)
