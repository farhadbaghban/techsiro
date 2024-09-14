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
from projectApps.products.api.serializers import CategorySerializer


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

    def test_create_category(self):
        self.client.force_authenticate(user=self.test_admin_user)

        url = reverse("ProductApis:category-list")
        data = {"name": "Books"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Category.objects.count(), 2)
        self.assertEqual(Category.objects.get(pk=response.data["id"]).name, "Books")

    def test_get_category(self):
        self.client.force_authenticate(user=self.test_admin_user)

        url = reverse("ProductApis:category-list")
        response = self.client.get(url)
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_update_category(self):
        self.client.force_authenticate(user=self.test_admin_user)

        url = reverse("ProductApis:category-detail", kwargs={"pk": self.category.id})
        data = {"name": "Updated Electronics"}
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.category.refresh_from_db()
        self.assertEqual(self.category.name, "Updated Electronics")

    def test_delete_category(self):
        self.client.force_authenticate(user=self.test_admin_user)

        url = reverse("ProductApis:category-detail", kwargs={"pk": self.category.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Category.objects.filter(pk=self.category.id).exists())
