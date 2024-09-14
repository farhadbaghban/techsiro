from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from projectApps.products.models import (
    Category,
    TypeAttribute,
    AttributeDefinition,
    AttributeValue,
    Product,
)
from projectApps.products.api.serializers import (
    CategorySerializer,
    TypeAttributeSerializer,
    AttributeDefinitionSerializer,
    AttributeValueSerializer,
    ProductSerializer,
)
from projectApps.products.api.permissions import IsAdminUser


class CategoryList(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryDetail(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, pk):
        try:
            category = Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = CategorySerializer(category)
        return Response(serializer.data)

    def put(self, request, pk):
        try:
            category = Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = CategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            category = Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TypeAttributeList(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        types = TypeAttribute.objects.all()
        serializer = TypeAttributeSerializer(types, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TypeAttributeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TypeAttributeDetail(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, pk):
        try:
            type_attr = TypeAttribute.objects.get(pk=pk)
        except TypeAttribute.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = TypeAttributeSerializer(type_attr)
        return Response(serializer.data)

    def put(self, request, pk):
        try:
            type_attr = TypeAttribute.objects.get(pk=pk)
        except TypeAttribute.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = TypeAttributeSerializer(type_attr, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            type_attr = TypeAttribute.objects.get(pk=pk)
        except TypeAttribute.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        type_attr.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AttributeDefinitionList(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        attribute_definitions = AttributeDefinition.objects.all()
        serializer = AttributeDefinitionSerializer(attribute_definitions, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = AttributeDefinitionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AttributeDefinitionDetail(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, pk):
        try:
            attribute_definition = AttributeDefinition.objects.get(pk=pk)
        except AttributeDefinition.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = AttributeDefinitionSerializer(attribute_definition)
        return Response(serializer.data)

    def put(self, request, pk):
        try:
            attribute_definition = AttributeDefinition.objects.get(pk=pk)
        except AttributeDefinition.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = AttributeDefinitionSerializer(
            attribute_definition, data=request.data
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            attribute_definition = AttributeDefinition.objects.get(pk=pk)
        except AttributeDefinition.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        attribute_definition.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AttributeValueList(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        attribute_values = AttributeValue.objects.all()
        serializer = AttributeValueSerializer(attribute_values, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = AttributeValueSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AttributeValueDetail(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, pk):
        try:
            attribute_value = AttributeValue.objects.get(pk=pk)
        except AttributeValue.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = AttributeValueSerializer(attribute_value)
        return Response(serializer.data)

    def put(self, request, pk):
        try:
            attribute_value = AttributeValue.objects.get(pk=pk)
        except AttributeValue.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = AttributeValueSerializer(attribute_value, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            attribute_value = AttributeValue.objects.get(pk=pk)
        except AttributeValue.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        attribute_value.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProductList(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductDetail(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, pk):
        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    def put(self, request, pk):
        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
