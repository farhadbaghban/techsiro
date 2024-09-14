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
from projectApps.products.api.serializers import AttributeDefinitionSerializer


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
        self.product.save()

    def test_create_attribute_definition(self):
        self.client.force_authenticate(user=self.test_admin_user)
        url = reverse("ProductApis:attribute-definition-list")
        data = {
            "name": "Size",
            "type": self.type_attribute.id,
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(AttributeDefinition.objects.count(), 2)
        self.assertEqual(
            AttributeDefinition.objects.get(pk=response.data["id"]).name, "Size"
        )

    def test_get_attribute_definition(self):
        self.client.force_authenticate(user=self.test_admin_user)
        url = reverse("ProductApis:attribute-definition-list")
        response = self.client.get(url)
        attribute_definitions = AttributeDefinition.objects.all()
        serializer = AttributeDefinitionSerializer(attribute_definitions, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_update_attribute_definition(self):
        self.client.force_authenticate(user=self.test_admin_user)
        url = reverse(
            "ProductApis:attribute-definition-detail",
            kwargs={"pk": self.attribute_definition.id},
        )
        data = {
            "name": "Updated Size",
            "type": self.type_attribute.id,
        }
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.attribute_definition.refresh_from_db()
        self.assertEqual(self.attribute_definition.name, "Updated Size")

    def test_delete_attribute_definition(self):
        self.client.force_authenticate(user=self.test_admin_user)
        url = reverse(
            "ProductApis:attribute-definition-detail",
            kwargs={"pk": self.attribute_definition.id},
        )
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(
            AttributeDefinition.objects.filter(pk=self.attribute_definition.id).exists()
        )
