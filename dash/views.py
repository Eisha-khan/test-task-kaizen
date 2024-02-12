from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework import permissions
from .models import *
from .serializers import*
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework import generics
# Create your views here.


class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    filter_backends = [DjangoFilterBackend,filters.SearchFilter,filters.OrderingFilter]
    search_fields = ['sku','name']
    permission_classes = [permissions.IsAuthenticated]

    # def list(self, request, *args, **kwargs):
    #     print(kwargs)
    #     data = list(Item.objects.all().values())
    #     return Response(data)
    class ItemList(generics.ListAPIView):
        pass

    def retrieve(self, request, *args, **kwargs):
        data = list(Item.objects.filter(id=kwargs['pk']).values())
        return Response(data)

    def create(self, request, *args, **kwargs):
        item_serializer_data = ItemSerializer(data=request.data)
        if item_serializer_data.is_valid():
            item_serializer_data.save()
            status_code = status.HTTP_201_CREATED
            return Response({"message": "Item Added Sucessfully", "status": status_code})
        else:
            status_code = status.HTTP_400_BAD_REQUEST
            return Response({"message": "Please fill the datails. Category may be incorrect", "status": status_code})

    def destroy(self, request, *args, **kwargs):
        item_data = Item.objects.filter(id=kwargs['pk'])
        if item_data:
            item_data.delete()
            status_code = status.HTTP_201_CREATED
            return Response({"message": "Item delete Sucessfully", "status": status_code})
        else:
            status_code = status.HTTP_400_BAD_REQUEST
            return Response({"message": "Item data not found", "status": status_code})

    def update(self, request, *args, **kwargs):
        item_details = Item.objects.get(id=kwargs['pk'])
        item_serializer_data = ItemSerializer(
            item_details, data=request.data, partial=True)
        if item_serializer_data.is_valid():
            item_serializer_data.save()
            status_code = status.HTTP_201_CREATED
            return Response({"message": "Item Update Sucessfully", "status": status_code})
        else:
            status_code = status.HTTP_400_BAD_REQUEST
            return Response({"message": "Item data Not found", "status": status_code})


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):
        data = list(Category.objects.all().values())
        return Response(data)

    def retrieve(self, request, *args, **kwargs):
        data = list(Category.objects.filter(id=kwargs['pk']).values())
        return Response(data)

    def create(self, request, *args, **kwargs):
        category_serializer_data = CategorySerializer(data=request.data)
        if category_serializer_data.is_valid():
            category_serializer_data.save()
            status_code = status.HTTP_201_CREATED
            return Response({"message": "Category Added Sucessfully", "status": status_code})
        else:
            status_code = status.HTTP_400_BAD_REQUEST
            return Response({"message": "please fill the datails", "status": status_code})

    def destroy(self, request, *args, **kwargs):
        category_data = Category.objects.filter(id=kwargs['pk'])
        if category_data:
            category_data.delete()
            status_code = status.HTTP_201_CREATED
            return Response({"message": "Category delete Sucessfully", "status": status_code})
        else:
            status_code = status.HTTP_400_BAD_REQUEST
            return Response({"message": "Category data not found", "status": status_code})

    def update(self, request, *args, **kwargs):
        category_details = Category.objects.get(id=kwargs['pk'])
        category_serializer_data = CategorySerializer(
            category_details, data=request.data, partial=True)
        if category_serializer_data.is_valid():
            category_serializer_data.save()
            status_code = status.HTTP_201_CREATED
            return Response({"message": "Category Update Sucessfully", "status": status_code})
        else:
            status_code = status.HTTP_400_BAD_REQUEST
            return Response({"message": "Category data Not found", "status": status_code})
