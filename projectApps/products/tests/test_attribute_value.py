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
from projectApps.products.api.serializers import AttributeValueSerializer


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

    def test_create_attribute_value(self):
        self.client.force_authenticate(user=self.test_admin_user)
        url = reverse("ProductApis:attribute-value-list")
        data = {
            "value": "Small",
            "attribute_definition": self.attribute_definition.id,
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(AttributeValue.objects.count(), 2)
        self.assertEqual(
            AttributeValue.objects.get(pk=response.data["id"]).value, "Small"
        )

    def test_get_attribute_value(self):
        self.client.force_authenticate(user=self.test_admin_user)
        url = reverse("ProductApis:attribute-value-list")
        response = self.client.get(url)
        attribute_values = AttributeValue.objects.all()
        serializer = AttributeValueSerializer(attribute_values, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_update_attribute_value(self):
        self.client.force_authenticate(user=self.test_admin_user)
        url = reverse(
            "ProductApis:attribute-value-detail", kwargs={"pk": self.attribute_value.id}
        )
        data = {
            "value": "Medium",
            "attribute_definition": self.attribute_definition.id,
        }
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.attribute_value.refresh_from_db()
        self.assertEqual(self.attribute_value.value, "Medium")

    def test_delete_attribute_value(self):
        self.client.force_authenticate(user=self.test_admin_user)
        url = reverse(
            "ProductApis:attribute-value-detail", kwargs={"pk": self.attribute_value.id}
        )
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(
            AttributeValue.objects.filter(pk=self.attribute_value.id).exists()
        )
