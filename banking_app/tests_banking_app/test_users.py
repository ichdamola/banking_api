from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token
from banking_app.models import User


class CreateUserAPIViewTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.create_user_url = reverse("create")

    def test_create_valid_user(self):
        data = {
            "first_name": "Adeola",
            "last_name": "Fadairo",
            "phone_number": "09036106263",
            "email": "testuser@example.com",
            "password": "testpass123",
        }
        response = self.client.post(self.create_user_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_invalid_user(self):
        data = {
            "username": "testuser",
            "email": "invalidemail",
            "password": "testpass123",
        }
        response = self.client.post(self.create_user_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class LoginUserAPIViewTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.login_user_url = reverse("login")
        self.user = User.objects.create_user(
            first_name="Adeola",
            last_name="Fadairo",
            phone_number="09036106263",
            email="testuser@example.com",
            password="testpass123",
        )

    def test_valid_login(self):
        data = {"email": "testuser@example.com", "password": "testpass123"}
        response = self.client.post(self.login_user_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_login(self):
        data = {"email": "testuser@example.com", "password": "wrongpass"}
        response = self.client.post(self.login_user_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class LogoutUserAPIViewTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.logout_user_url = reverse("logout")
        self.user = User.objects.create_user(
            first_name="Adeola",
            last_name="Fadairo",
            phone_number="09036106263",
            email="testuser@example.com",
            password="testpass123",
        )
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

    def test_unauthenticated_logout(self):
        response = self.client.post(self.logout_user_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_invalid_logout(self):
        self.client.credentials()
        response = self.client.post(self.logout_user_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class GetUserAPIViewTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.get_user_url = reverse("get_logged_user")
        self.user = User.objects.create_user(
            first_name="Adeola",
            last_name="Fadairo",
            phone_number="09036106263",
            email="testuser@example.com",
            password="testpass123",
        )
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

    def test_get_user(self):
        response = self.client.get(self.get_user_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class DeleteCurrentUserAPIViewTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.delete_user_url = reverse("delete-current-user")
        self.user = User.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="testpass123",
        )
