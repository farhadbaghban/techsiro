from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from projectApps.cart.models import Order, OrderItem
from projectApps.products.models import (
    Product,
    Category,
    TypeAttribute,
    AttributeDefinition,
    AttributeValue,
)
from django.contrib.auth import get_user_model

User = get_user_model()


class OrderItemTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email="testuser@email.com", password="testpass"
        )
        self.client.force_authenticate(user=self.user)
        self.order = Order.objects.create(user=self.user)
        self.category = Category.objects.create(name="Electronics")
        self.type_attribute = TypeAttribute.objects.create(name="Color")
        self.attribute_definition = AttributeDefinition.objects.create(
            name="Color", type=self.type_attribute
        )
        self.attribute_value = AttributeValue.objects.create(
            value="Red", attribute_definition=self.attribute_definition
        )
        self.product = Product.objects.create(
            name="Test Product",
            category=self.category,
        )

        self.product.attributes.set([self.attribute_value])
        self.orderitem_url = reverse(
            "CartAPI:orderitem-list-create", args=[self.order.pk]
        )

    def test_create_order_item(self):
        response = self.client.post(
            self.orderitem_url,
            {"product": self.product.pk, "quantity": 2, "order": self.order.id},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_order_items(self):
        OrderItem.objects.create(order=self.order, product=self.product, quantity=1)
        response = self.client.get(self.orderitem_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_order_item(self):
        item = OrderItem.objects.create(
            order=self.order, product=self.product, quantity=1
        )
        response = self.client.put(
            reverse("CartAPI:orderitem-detail", args=[self.order.pk, item.pk]),
            {"quantity": 3},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_order_item(self):
        item = OrderItem.objects.create(
            order=self.order, product=self.product, quantity=1
        )
        response = self.client.delete(
            reverse("CartAPI:orderitem-detail", args=[self.order.pk, item.pk])
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
