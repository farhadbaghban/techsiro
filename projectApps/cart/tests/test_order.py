from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from projectApps.cart.models import Order
from django.contrib.auth import get_user_model

User = get_user_model()


class OrderTests(APITestCase):
    def setUp(self):
        self.client = APIClient()

        self.user = User.objects.create_user(
            email="testuser@email.com", password="testpass"
        )
        self.client.force_authenticate(user=self.user)
        self.order_url = reverse("CartAPI:order-list-create")

    def test_create_order(self):
        response = self.client.post(
            self.order_url, {"items": [], "options": []}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_orders(self):
        Order.objects.create(user=self.user)
        response = self.client.get(self.order_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_order(self):
        order = Order.objects.create(user=self.user)
        response = self.client.put(
            reverse("CartAPI:order-detail", args=[order.pk]),
            {"items": [], "options": []},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)

    def test_delete_order(self):
        order = Order.objects.create(user=self.user)
        response = self.client.delete(reverse("CartAPI:order-detail", args=[order.pk]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
