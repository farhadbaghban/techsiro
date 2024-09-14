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
from projectApps.products.api.serializers import TypeAttributeSerializer


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

    def test_create_type_attribute(self):
        self.client.force_authenticate(user=self.test_admin_user)
        url = reverse("ProductApis:type-attribute-list")
        data = {"name": "Size"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(TypeAttribute.objects.count(), 2)
        self.assertEqual(TypeAttribute.objects.get(pk=response.data["id"]).name, "Size")

    def test_get_type_attribute(self):
        self.client.force_authenticate(user=self.test_admin_user)
        url = reverse("ProductApis:type-attribute-list")
        response = self.client.get(url)
        type_attributes = TypeAttribute.objects.all()
        serializer = TypeAttributeSerializer(type_attributes, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_update_type_attribute(self):
        self.client.force_authenticate(user=self.test_admin_user)
        url = reverse(
            "ProductApis:type-attribute-detail", kwargs={"pk": self.type_attribute.id}
        )
        data = {"name": "Updated Color"}
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.type_attribute.refresh_from_db()
        self.assertEqual(self.type_attribute.name, "Updated Color")

    def test_delete_type_attribute(self):
        self.client.force_authenticate(user=self.test_admin_user)

        url = reverse(
            "ProductApis:type-attribute-detail", kwargs={"pk": self.type_attribute.id}
        )
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(
            TypeAttribute.objects.filter(pk=self.type_attribute.id).exists()
        )
