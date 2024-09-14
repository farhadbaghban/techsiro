# projectApps/orders/serializers.py

from rest_framework import serializers
from projectApps.cart.models import Order, OrderItem, OrderOption


class OrderOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderOption
        fields = ["id", "key", "value", "order"]


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ["id", "product", "quantity", "order"]


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    options = OrderOptionSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ["id", "created_at", "items", "options"]
