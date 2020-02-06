from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ..Serializers.MapSerializer import MapSerializer, MapSerializerGet, MapItemsSerializer, MapFullSerializerGet
from calculation.models.map import Map, MapItems


class MapViewGet(APIView):
    def get(self, request):
        queryset = Map.objects.all()
        serializer_class = MapSerializerGet(queryset, many=True)
        return Response(serializer_class.data)


class MapFullViewGet(APIView):
    def get(self, request, id):
        instance = Map.objects.get(id=id)
        serializer_class = MapFullSerializerGet(instance, many=False)
        return Response(serializer_class.data)


class MapSelectGet(APIView):
    def get(self, request):
        if request.GET.get('q'):
            queryset = Map.objects.filter(name__icontains=request.GET.get('q'))
        else:
            queryset = Map.objects.all()

        elements = []

        for obj in queryset:
            elements.append({'id': obj.id, "text": obj.name})
        return Response({"results": elements})


class MapViewSet(APIView):
    # authentication_classes = (TokenAuthentication,)
    # permission_classes = (IsAuthenticated,)

    def get(self, request):
        queryset = Map.objects.all()
        serializer_class = MapSerializerGet(queryset, many=True)

        return Response(serializer_class.data)

    def post(self, request):
        map_obj = request.data.get('map')
        serializer = MapSerializer(data=map_obj)

        for item in request.data.get('items'):
            item_serializer = MapItemsSerializer(data=item)
            if item_serializer.is_valid(raise_exception=True):
                pass

        if serializer.is_valid(raise_exception=True):
            saved_map_obj = serializer.save()
            for item in request.data.get('items'):
                item = json_modify(item, 'map_doc', saved_map_obj.id)
                item_serializer = MapItemsSerializer(data=item)
                if item_serializer.is_valid(raise_exception=True):
                    item_serializer.save()
        return Response({"status": "done", "data": serializer.data})

    def put(self, request, id):

        map_instance = get_object_or_404(Map.objects.all(), pk=id)
        map_request = request.data.get('map')
        serializer = MapSerializer(instance=map_instance, data=map_request, partial=True)
        if serializer.is_valid(raise_exception=True):
            saved_map_obj = serializer.save()
            for item in request.data.get('items'):
                print(item.get('id'))
                item = json_modify(item, 'map_doc', saved_map_obj.id)

                if int(item.get('id')) > -1:
                    item_instance = get_object_or_404(MapItems.objects.all(), pk=int(item.get('id')))
                    item_serializer = MapItemsSerializer(instance=item_instance, data=item, partial=True)
                    if item_serializer.is_valid(raise_exception=True):
                        item_serializer.save()
                else:
                    item_serializer = MapItemsSerializer(data=item)
                    if item_serializer.is_valid(raise_exception=True):
                        item_serializer.save()
        return Response({"status": "done", "data": 'serializer.data'})

    def delete(self, request, id):
        # Get object with this pk
        type_item = get_object_or_404(Map.objects.all(), pk=id)
        type_item.delete()
        return Response({
            "message": "TypeItem with id `{}` has been deleted.".format(id)
        }, status=204)


def json_modify(json_obj: dict, key, value):
    import json
    json_str = json.dumps(json_obj)
    if type(key) == str:
        json_str = json_str[0:len(json_str) - 1] + ', "{}":"{}"'.format(key, value) + '}'
    else:
        json_str = json_str[0:len(json_str) - 1] + ', "{}":{}'.format(key, value) + '}'
    return json.loads(json_str)
