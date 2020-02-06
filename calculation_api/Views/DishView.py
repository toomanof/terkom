from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ..Serializers.DishSerializer import DishSerializer, DishSerializerGet
from calculation.models.dish import Dish
from root import settings
from ..MyPaginationMixin import MyPaginationMixin
from rest_framework.settings import api_settings


class DishViewSetGet(APIView):
    def get(self, request):
        queryset = Dish.objects.all()
        serializer_class = DishSerializerGet(queryset, many=True)
        return Response(serializer_class.data)


class DishSelect2Get(APIView):
    def get(self, request):
        if request.GET.get('q'):
            queryset = Dish.objects.filter(name__icontains=request.GET.get('q'))
        else:
            queryset = Dish.objects.all()

        elements = []
        for obj in queryset:
            elements.append({'id': obj.id, "text": obj.name})

        return Response({"results": elements, "pagination": {"more": False}})


class DishViewSet(APIView):
    # authentication_classes = (TokenAuthentication,)
    # permission_classes = (IsAuthenticated,)

    def post(self, request):
        map_obj = request.data
        serializer = DishSerializer(data=map_obj)
        if serializer.is_valid(raise_exception=True):
            try:
                saved_data = serializer.save()
            except Exception as ex:
                return Response({"status": "failed", "data": str(ex)}, status=409)
        serializer_class = DishSerializerGet(saved_data, many=False)
        return Response({"status": "done", "data": serializer_class.data})

    def put(self, request, id):
        saved_dish_obj = get_object_or_404(Dish.objects.all(), pk=id)
        data = request.data

        serializer = DishSerializer(instance=saved_dish_obj, data=data, partial=True)
        if serializer.is_valid(raise_exception=True):
            try:
                saved_data = serializer.save()
            except Exception as ex:
                return Response({"status": "failed", "data": str(ex)}, status=409)
        serializer_class = DishSerializerGet(saved_data, many=False)

        return Response({"status": "done", "data": serializer_class.data})

    def delete(self, request, id):
        # Get object with this pk
        dish_obj = get_object_or_404(Dish.objects.all(), pk=id)
        dish_obj.delete()
        return Response({
            "message": "TypeItem with id `{}` has been deleted.".format(id)
        }, status=204)
