# projectApps/cart/tests.py
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from projectApps.cart.models import Order, OrderOption
from django.contrib.auth import get_user_model

User = get_user_model()


class OrderOptionTests(APITestCase):
    def setUp(self):
        self.client = APIClient()

        self.user = User.objects.create_user(
            email="testuser@email.com", password="testpass"
        )
        self.client.force_authenticate(user=self.user)
        self.order = Order.objects.create(user=self.user)
        self.orderoption_url = reverse(
            "CartAPI:orderoption-list-create", args=[self.order.pk]
        )

    def test_create_order_option(self):
        response = self.client.post(
            self.orderoption_url,
            {
                "key": "Color",
                "value": "Red",
                "order": self.order.id,
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_order_options(self):
        OrderOption.objects.create(order=self.order, key="Size", value="Large")
        response = self.client.get(self.orderoption_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_order_option(self):
        option = OrderOption.objects.create(order=self.order, key="Size", value="Large")
        response = self.client.put(
            reverse("CartAPI:orderoption-detail", args=[self.order.pk, option.pk]),
            {
                "value": "Small",
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_order_option(self):
        option = OrderOption.objects.create(order=self.order, key="Size", value="Large")
        response = self.client.delete(
            reverse("CartAPI:orderoption-detail", args=[self.order.pk, option.pk])
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
