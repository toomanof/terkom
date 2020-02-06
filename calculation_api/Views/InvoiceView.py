from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ..Serializers.InvoiceSerializer import InvoiceSerializerGet, InvoiceItemsSerializerGet
from calculation.models.invoice import Invoice, InvoiceItems


class InvoiceViewGet(APIView):
    def get(self, request):
        queryset = Invoice.objects.all()
        serializer_class = InvoiceSerializerGet(queryset, many=True)
        return Response(serializer_class.data)


class InvoiceItemsViewGet(APIView):
    def get(self, request):
        queryset = InvoiceItems.objects.all()
        serializer_class = InvoiceItemsSerializerGet(queryset, many=True)
        return Response(serializer_class.data)
