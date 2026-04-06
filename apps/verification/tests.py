from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from apps.accounts.models import User
from apps.drugs.models import Drug, BatchNumber
from datetime import date

class VerificationTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.manufacturer = User.objects.create_user(email="mfr@example.com", password="pass1234", role="manufacturer", company_name="Test Pharma")
        self.pharmacist = User.objects.create_user(email="pharm@example.com", password="pass1234", role="pharmacist")
        self.drug = Drug.objects.create(name="Aspirin", nafdac_number="C1-0001", manufacturer=self.manufacturer, dosage_form="Tablet", strength="100mg")
        self.batch = BatchNumber.objects.create(drug=self.drug, batch_number="TEST-001", manufacture_date=date(2026,1,1), expiry_date=date(2028,1,1), quantity=500)

    def authenticate(self, email, password):
        response = self.client.post("/api/auth/login/", {"email": email, "password": password})
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + response.data["access"])

    def test_verify_authentic_batch(self):
        self.authenticate("pharm@example.com", "pass1234")
        response = self.client.post("/api/verification/verify/", {"scanned_code": "TEST-001", "location": "Lagos"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["result"], "authentic")

    def test_verify_not_found(self):
        self.authenticate("pharm@example.com", "pass1234")
        response = self.client.post("/api/verification/verify/", {"scanned_code": "FAKE-999", "location": "Lagos"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["result"], "not_found")

    def test_verify_recalled_batch(self):
        self.batch.status = "recalled"
        self.batch.save()
        self.authenticate("pharm@example.com", "pass1234")
        response = self.client.post("/api/verification/verify/", {"scanned_code": "TEST-001", "location": "Lagos"})
        self.assertEqual(response.data["result"], "recalled")

    def test_verification_history(self):
        self.authenticate("pharm@example.com", "pass1234")
        self.client.post("/api/verification/verify/", {"scanned_code": "TEST-001", "location": "Lagos"})
        response = self.client.get("/api/verification/history/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
