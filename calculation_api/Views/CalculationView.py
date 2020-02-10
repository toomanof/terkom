from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ..Serializers.CalculationSerializer import CalculationSerializer
from calculation.models.calculation import Calculation


class CalculationViewSet(APIView):
    # authentication_classes = (TokenAuthentication,)
    # permission_classes = (IsAuthenticated,)

    def get(self, request):
        queryset = Calculation.objects.all()
        serializer_class = CalculationSerializer(queryset, many=True)
        content = {
            'status': 'done',
            'amount': len(queryset),
            'data': serializer_class.data
        }

        return Response(content)

    def post(self, request):
        calculation_obj = request.data
        serializer = CalculationSerializer(data=calculation_obj)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response({"status": "done", "data": serializer.data})

    def put(self, request, id):
        saved_calculation_obj = get_object_or_404(Calculation.objects.all(), pk=id)
        data = request.data
        serializer = CalculationSerializer(instance=saved_calculation_obj, data=data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response({"status": "done", "data": serializer.data})

    def delete(self, request, id):
        # Get object with this pk
        calculation_obj = get_object_or_404(Calculation.objects.all(), pk=id)
        calculation_obj.delete()
        return Response({
            "message": "TypeItem with id `{}` has been deleted.".format(id)
        }, status=204)
