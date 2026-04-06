from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from apps.accounts.models import User

class AccountsTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email="test@example.com",
            password="pass1234",
            role="manufacturer",
            company_name="Test Co"
        )

    def test_user_creation(self):
        self.assertEqual(self.user.email, "test@example.com")
