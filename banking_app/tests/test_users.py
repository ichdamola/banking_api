from rest_framework import status

from banking_app.tests.test_setup import SetUp


class UserAPIViewTestCase(SetUp):
    def test_create_valid_user(self):
        response = self.client.post(
            self.create_user_url, self.data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_user_incomplete_data(self):
        data = {"email": "invalidemail", "password": "testpass123"}
        response = self.client.post(self.create_user_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_valid_login(self):
        data = {"email": "testuser@example.com", "password": "testpass123"}
        response = self.client.post(self.login_user_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_valid_logout(self):
        response = self.client.post(self.logout_user_url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
