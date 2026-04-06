from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from apps.accounts.models import User
from apps.drugs.models import Drug

class DrugTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.manufacturer = User.objects.create_user(
            email="mfr@example.com",
            password="pass1234",
            role="manufacturer",
            company_name="Test Pharma"
        )
        self.drug_data = {
            "name": "Aspirin",
            "generic_name": "Acetylsalicylic acid",
            "nafdac_number": "B1-0001",
            "description": "Pain relief",
            "dosage_form": "Tablet",
            "strength": "100mg"
        }

    def authenticate(self):
        response = self.client.post("/api/auth/login/", {
            "email": "mfr@example.com",
            "password": "pass1234"
        })
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + response.data["access"])

    def test_manufacturer_can_create_drug(self):
        self.authenticate()
        response = self.client.post("/api/drugs/", self.drug_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], "Aspirin")

    def test_verify_drug_by_nafdac(self):
        self.authenticate()
        self.client.post("/api/drugs/", self.drug_data)
        response = self.client.get("/api/drugs/verify/B1-0001/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["nafdac_number"], "B1-0001")
