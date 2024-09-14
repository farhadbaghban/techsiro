from django.urls import reverse

from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from projectApps.comments.models import Comment
from projectApps.products.models import (
    Product,
    Category,
    TypeAttribute,
    AttributeDefinition,
    AttributeValue,
)

User = get_user_model()

app_name = "CommentsAPI"


class CommentTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email="testuser@email.com", password="password"
        )
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
        self.client.force_authenticate(user=self.user)
        self.comment = Comment.objects.create(
            user=self.user, product=self.product, content="Test comment"
        )

    def test_create_comment(self):
        url = reverse(f"{app_name}:comment-list")
        data = {
            "product": self.product.id,
            "content": "Another test comment",
            "is_response": False,
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.count(), 2)
        self.assertEqual(Comment.objects.latest("id").content, "Another test comment")

    def test_get_comments(self):
        url = reverse(f"{app_name}:comment-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_comment_detail(self):
        url = reverse(f"{app_name}:comment-detail", kwargs={"pk": self.comment.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["content"], "Test comment")

    def test_update_comment(self):
        url = reverse(f"{app_name}:comment-detail", kwargs={"pk": self.comment.id})
        data = {"content": "Updated comment"}
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            Comment.objects.get(id=self.comment.id).content, "Updated comment"
        )

    def test_delete_comment(self):
        url = reverse(f"{app_name}:comment-detail", kwargs={"pk": self.comment.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Comment.objects.count(), 0)
