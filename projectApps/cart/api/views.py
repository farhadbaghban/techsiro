from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from projectApps.cart.models import Order, OrderItem, OrderOption
from projectApps.cart.api.serializers import (
    OrderSerializer,
    OrderItemSerializer,
    OrderOptionSerializer,
)
from projectApps.accounts.models import User


class OrderListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        orders = Order.objects.filter(user=request.user)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk: int, user: User):
        try:
            return Order.objects.get(pk=pk, user=user)
        except Order.DoesNotExist:
            return Response(
                exception=Order.DoesNotExist, status=status.HTTP_404_NOT_FOUND
            )

    def get(self, request, pk):
        user = request.user
        order = self.get_object(pk, user)
        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        user = request.user
        order = self.get_object(pk, user)
        serializer = OrderSerializer(order, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        user = request.user
        order = self.get_object(pk, user)
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class OrderItemListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, order_pk):
        items = OrderItem.objects.filter(order__user=request.user, order_id=order_pk)
        serializer = OrderItemSerializer(items, many=True)
        return Response(serializer.data)

    def post(self, request, order_pk):
        data = request.data.copy()
        data["order"] = order_pk
        serializer = OrderItemSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderItemDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, order_pk, pk):
        try:
            return OrderItem.objects.get(
                pk=pk, order_id=order_pk, order__user=self.request.user
            )
        except OrderItem.DoesNotExist:
            return None

    def get(self, request, order_pk, pk):
        item = self.get_object(order_pk, pk)
        if item is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = OrderItemSerializer(item)
        return Response(serializer.data)

    def put(self, request, order_pk, pk):
        item = self.get_object(order_pk, pk)
        if item is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = OrderItemSerializer(item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, order_pk, pk):
        item = self.get_object(order_pk, pk)
        if item is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# OrderOption Views
class OrderOptionListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, order_pk):
        options = OrderOption.objects.filter(
            order__user=request.user, order_id=order_pk
        )
        serializer = OrderOptionSerializer(options, many=True)
        return Response(serializer.data)

    def post(self, request, order_pk):
        data = request.data.copy()
        data["order"] = order_pk
        serializer = OrderOptionSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderOptionDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, order_pk, pk):
        try:
            return OrderOption.objects.get(
                pk=pk, order_id=order_pk, order__user=self.request.user
            )
        except OrderOption.DoesNotExist:
            return None

    def get(self, request, order_pk, pk):
        option = self.get_object(order_pk, pk)
        if option is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = OrderOptionSerializer(option)
        return Response(serializer.data)

    def put(self, request, order_pk, pk):
        option = self.get_object(order_pk, pk)
        if option is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = OrderOptionSerializer(option, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, order_pk, pk):
        option = self.get_object(order_pk, pk)
        if option is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        option.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
