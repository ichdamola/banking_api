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
        data = {
            "account_name": "Test Account",
            "amount": 1000,
            "user": self.user.id,
        }
        response = self.client.post(self.accounts_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        account = Account.objects.get(id=response.data["id"])
        serializer = AccountSerializer(account)
        self.assertEqual(response.data, serializer.data)

    def test_retrieve_account(self):
        """
        Ensure we can retrieve an existing account object.
        """
        account = Account.objects.create(
            account_name="Test Account", user=self.user
        )
        url = reverse("accounts-detail", args=[account.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["account_name"], account.account_name)

    def test_update_account(self):
        """
        Ensure we can update an existing account object.
        """
        account = Account.objects.create(
            account_name="Test Account", user=self.user
        )
        url = reverse("accounts-detail", args=[account.id])
        data = {"account_name": "Updated Test Account", "user": self.user.id}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["account_name"], data["account_name"])

    def test_delete_account(self):
        """
        Ensure we can delete an existing account object.
        """
        account = Account.objects.create(
            account_name="Test Account", user=self.user
        )
        url = reverse("accounts-detail", args=[account.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
