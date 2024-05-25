from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth import get_user_model
from .models import Workplace

class WorkplaceAPITests(APITestCase):

    def setUp(self):
        self.user_model = get_user_model()
        self.user = self.user_model.objects.create_user(
            email='employer@example.com',
            password='Testpassword123!',
            is_employer=True
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.workplace = Workplace.objects.create(
            street='Main',
            street_number='123',
            postal_code='123 45',
            city='Sample City'
        )

    def test_list_workplaces(self):
        url = reverse('workplace-list')  # Change to the correct name if needed
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['street'], 'Main')

    def test_create_workplace(self):
        url = reverse('workplace-list')  # Change to the correct name if needed
        data = {
            'street': 'New Street',
            'street_number': '456',
            'postal_code': '678 90',
            'city': 'New City'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Workplace.objects.count(), 2)

    def test_retrieve_workplace(self):
        url = reverse('workplace-detail', args=[self.workplace.id])  # Change to the correct name if needed
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['street'], 'Main')

    def test_update_workplace(self):
        url = reverse('workplace-detail', args=[self.workplace.id])  # Change to the correct name if needed
        data = {
            'street': 'Updated Street',
            'street_number': '123',
            'postal_code': '123 45',
            'city': 'Sample City'
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.workplace.refresh_from_db()
        self.assertEqual(self.workplace.street, 'Updated Street')

    def test_delete_workplace(self):
        url = reverse('workplace-detail', args=[self.workplace.id])  # Change to the correct name if needed
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Workplace.objects.filter(id=self.workplace.id).exists())
