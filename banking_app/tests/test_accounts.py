from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from banking_app.models import Account
from banking_app.serializers import AccountSerializer
from banking_app.tests.test_setup import SetUp
from banking_app.models import User
from banking_app.services import generate_account_number


class AccountTests(SetUp):
    accounts_url = reverse("accounts-list")

    def test_create_account(self):
        user = User.objects.create_user(
            first_name=self.fake.unique.first_name(),
            last_name=self.fake.unique.last_name(),
            phone_number=self.fake.phone_number(),
            email=self.fake.email(),
            password="testpass123",
        )
        data = {
            "account_name": "Test Account",
            "amount": 1000,
            "user": user.id,
        }
        response = self.client.post(self.accounts_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        account = Account.objects.get(id=response.data["id"])
        serializer = AccountSerializer(account)
        self.assertEqual(response.data, serializer.data)
