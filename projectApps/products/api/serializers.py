from rest_framework import serializers
from projectApps.products.models import (
    Category,
    TypeAttribute,
    AttributeDefinition,
    AttributeValue,
    Product,
)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "parent"]


class TypeAttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeAttribute
        fields = ["id", "name"]


class AttributeDefinitionSerializer(serializers.ModelSerializer):
    type = serializers.PrimaryKeyRelatedField(queryset=TypeAttribute.objects.all())

    class Meta:
        model = AttributeDefinition
        fields = ["id", "name", "type"]


class AttributeValueSerializer(serializers.ModelSerializer):
    attribute_definition = serializers.PrimaryKeyRelatedField(
        queryset=AttributeDefinition.objects.all()
    )

    class Meta:
        model = AttributeValue
        fields = ["id", "value", "attribute_definition"]


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    attributes = serializers.PrimaryKeyRelatedField(queryset=AttributeValue.objects.all(),many=True)

    class Meta:
        model = Product
        fields = ["id", "name", "category", "attributes"]
