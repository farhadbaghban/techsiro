from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from projectApps.products.models import (
    Category,
    TypeAttribute,
    AttributeDefinition,
    AttributeValue,
    Product,
)
from projectApps.accounts.models import User
from projectApps.products.api.serializers import ProductSerializer


class APITests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.test_admin_user = User.objects.create_superuser(
            email="test@example.com", password="password123"
        )
        # Setup initial data for the tests
        self.category = Category.objects.create(name="Electronics")
        self.type_attribute = TypeAttribute.objects.create(name="Color")
        self.attribute_definition = AttributeDefinition.objects.create(
            name="Color", type=self.type_attribute
        )
        self.attribute_value = AttributeValue.objects.create(
            value="Red", attribute_definition=self.attribute_definition
        )
        self.product = Product.objects.create(name="Smartphone", category=self.category)
        self.product.attributes.add(self.attribute_value)

    def test_create_product(self):
        self.client.force_authenticate(user=self.test_admin_user)

        url = reverse("ProductApis:product-list")
        data = {
            "name": "Laptop",
            "category": self.category.id,
            "attributes": [self.attribute_value.id],
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 2)
        self.assertEqual(Product.objects.get(pk=response.data["id"]).name, "Laptop")

    def test_get_product(self):
        self.client.force_authenticate(user=self.test_admin_user)

        url = reverse("ProductApis:product-list")
        response = self.client.get(url)
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_update_product(self):
        self.client.force_authenticate(user=self.test_admin_user)

        url = reverse("ProductApis:product-detail", kwargs={"pk": self.product.id})
        data = {
            "name": "Updated Smartphone",
            "category": self.category.id,
            "attributes": [self.attribute_value.id],
        }
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.product.refresh_from_db()
        self.assertEqual(self.product.name, "Updated Smartphone")

    def test_delete_product(self):
        self.client.force_authenticate(user=self.test_admin_user)

        url = reverse("ProductApis:product-detail", kwargs={"pk": self.product.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Product.objects.filter(pk=self.product.id).exists())
