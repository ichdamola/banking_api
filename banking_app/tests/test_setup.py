from django.urls import reverse
from django.conf import settings

from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token
from faker import Faker
import jwt

from banking_app.models import User


class SetUp(APITestCase):
    fake = Faker()
    client = APIClient()
    login_user_url = reverse("login")
    logout_user_url = reverse("logout")
    create_user_url = reverse("create")
    data = {
        "first_name": fake.unique.first_name(),
        "last_name": fake.unique.last_name(),
        "phone_number": fake.phone_number(),
        "email": fake.email(),
        "password": fake.password(),
    }

    def setUp(self):
        self.user = User.objects.create_user(
            first_name=self.fake.unique.first_name(),
            last_name=self.fake.unique.last_name(),
            phone_number=self.fake.phone_number(),
            email="testuser@example.com",
            password="testpass123",
        )
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        self.client.cookies["jwt"] = jwt.encode(
            {"id": self.user.id}, settings.JWT_SECRET, algorithm="HS256"
        )
