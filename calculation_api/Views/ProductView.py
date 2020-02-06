from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from ..Serializers.ProductSerializer import ProductSerializerGet, ProductSerializerSet, ProductSerializerForSelect
from calculation.models.product import Product


class ProductSelect2Get(APIView):
    def get(self, request):
        if request.GET.get('q'):
            queryset = Product.objects.filter(name__icontains=request.GET.get('q'))
        else:
            queryset = Product.objects.all()

        serializer_class = ProductSerializerForSelect(queryset, many=True)
        return Response({"results": serializer_class.data, "pagination": {"more": False}})


class ProductViewGet(APIView):
    def get(self, request):
        queryset = Product.objects.all()
        serializer_class = ProductSerializerGet(queryset, many=True)
        return Response(serializer_class.data)

    def post(self, request):
        product_obj = request.data

        serializer = ProductSerializerSet(data=product_obj)
        if serializer.is_valid(raise_exception=True):
            try:
                saved_data = serializer.save()
            except Exception as ex:
                return Response({"status": "failed", "data": str(ex)}, status=status.HTTP_409_CONFLICT)
        serializer_class = ProductSerializerGet(saved_data, many=False)
        return Response({"status": "done", "data": serializer_class.data},status=status.HTTP_201_CREATED)

    def put(self, request, id):
        product_obj = get_object_or_404(Product.objects.all(), pk=id)
        data = request.data
        serializer = ProductSerializerSet(instance=product_obj, data=data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response({"status": "done", "data": serializer.data})

    def delete(self, request, id):
        # Get object with this pk
        item_history = get_object_or_404(Product.objects.all(), pk=id)
        item_history.delete()
        return Response({
            "message": "ItemHistory with id `{}` has been deleted.".format(id)
        }, status=204)
# class ProductViewSet(APIView):
