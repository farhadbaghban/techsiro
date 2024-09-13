from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from projectApps.accounts.models import User

app_name = "AccountUserApi"


class UserTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse(f"{app_name}:user-register")
        self.login_url = reverse(f"{app_name}:user-login")
        self.user_list_url = reverse(f"{app_name}:user-list")
        self.delete_user_url = reverse(f"{app_name}:user-delete")

        # Create a user to test with
        self.test_user = User.objects.create_user(
            email="test@example.com", password="password123"
        )

    def test_user_registration(self):
        data = {
            "email": "newuser@example.com",
            "password": "newpassword123",
        }
        response = self.client.post(self.register_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_user_registration_with_existing_email(self):
        data = {
            "email": "test@example.com",  # Already registered email
            "password": "password123",
        }
        response = self.client.post(self.register_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], "You registered Before")

    def test_user_login(self):
        data = {
            "email": "test@example.com",
            "password": "password123",
        }
        response = self.client.post(self.login_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_user_login_invalid_credentials(self):
        data = {
            "email": "test@example.com",
            "password": "wrongpassword",
        }
        response = self.client.post(self.login_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data["error"], "Invalid credentials")

    def test_user_list(self):
        self.client.force_authenticate(user=self.test_user)
        response = self.client.get(self.user_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], "test@example.com")

    def test_user_delete(self):
        self.client.force_authenticate(user=self.test_user)
        response = self.client.delete(self.delete_user_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Your account deleted successfully.")

        # Check if user is deactivated
        self.test_user.refresh_from_db()
        self.assertFalse(self.test_user.is_active)
        self.assertIsNotNone(self.test_user.de_activate_date)
