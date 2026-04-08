import os
import django
from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from apps.drugs.models import Drug, BatchNumber
from apps.verification.models import VerificationLog

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

User = get_user_model()

class DrugVerificationTests(APITestCase):
    def setUp(self):
        # Create test users
        self.manufacturer = User.objects.create_user(
            email='manufacturer@test.com',
            password='testpass123',
            role='manufacturer',
            company_name='Test Pharma'
        )
        self.pharmacist = User.objects.create_user(
            email='pharmacist@test.com',
            password='testpass123',
            role='pharmacist'
        )

        # Create test drug
        self.drug = Drug.objects.create(
            name='Test Drug',
            nafdac_number='TEST123',
            manufacturer=self.manufacturer,
            dosage_form='Tablet',
            strength='10mg'
        )

        # Create test batch
        self.batch = BatchNumber.objects.create(
            drug=self.drug,
            batch_number='BATCH001',
            manufacture_date='2024-01-01',
            expiry_date='2025-01-01',
            quantity=100
        )

    def test_drug_creation(self):
        """Test that manufacturers can create drugs"""
        self.client.force_authenticate(user=self.manufacturer)
        data = {
            'name': 'New Drug',
            'nafdac_number': 'NEW123',
            'dosage_form': 'Capsule',
            'strength': '20mg'
        }
        response = self.client.post('/api/drugs/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Drug.objects.filter(manufacturer=self.manufacturer).count(), 2)

    def test_qr_generation(self):
        """Test QR code generation for batches"""
        self.client.force_authenticate(user=self.manufacturer)
        response = self.client.get(f'/api/drugs/batches/{self.batch.id}/qr/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('qr_image_base64', response.data)
        self.assertIn('qr_data', response.data)

    def test_drug_verification_authentic(self):
        """Test verification of authentic drug"""
        self.client.force_authenticate(user=self.pharmacist)
        data = {'scanned_code': 'BATCH001', 'location': 'Test Location'}
        response = self.client.post('/api/verification/verify/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['result'], 'authentic')

        # Check log was created
        log = VerificationLog.objects.filter(scanned_code='BATCH001').first()
        self.assertIsNotNone(log)
        self.assertEqual(log.result, 'authentic')

    def test_drug_verification_not_found(self):
        """Test verification of non-existent batch"""
        self.client.force_authenticate(user=self.pharmacist)
        data = {'scanned_code': 'NONEXISTENT', 'location': 'Test Location'}
        response = self.client.post('/api/verification/verify/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['result'], 'not_found')

    def test_verification_history(self):
        """Test fetching verification history"""
        # Create some verification logs
        VerificationLog.objects.create(
            batch=self.batch,
            verified_by=self.pharmacist,
            scanned_code='BATCH001',
            result='authentic',
            location='Test'
        )

        self.client.force_authenticate(user=self.pharmacist)
        response = self.client.get('/api/verification/history/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_unauthorized_access(self):
        """Test that unauthorized users can't access manufacturer endpoints"""
        # Try to create drug without authentication
        data = {'name': 'Unauthorized Drug', 'nafdac_number': 'UNAUTH123'}
        response = self.client.post('/api/drugs/', data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

if __name__ == '__main__':
    import unittest
    unittest.main()