from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth import get_user_model
from .models import Profile
from worksession.models import WorkSession

class ProfileAPITests(APITestCase):

    def setUp(self):
        self.user_model = get_user_model()
        self.user = self.user_model.objects.create_user(
            email='testuser@example.com',
            password='Testpassword123!',
            is_employer=False
        )
        self.profile = Profile.objects.create(
            user=self.user,
            first_name='John',
            last_name='Doe',
            personnummer='900101-1234'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_register_user(self):
        url = reverse('register')
        data = {
            'email': 'newuser@example.com',
            'password': 'Testpassword123!',
            'first_name': 'New',
            'last_name': 'User',
            'personnummer': '900102-1234'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Profile.objects.count(), 2)

    def test_list_profiles(self):
        url = reverse('profile-list')  # Change to the correct name if needed
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['first_name'], 'John')

    def test_retrieve_profile(self):
        url = reverse('profile-detail', args=[self.profile.id])  # Change to the correct name if needed
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], 'John')

    def test_update_profile(self):
        url = reverse('profile-detail', args=[self.profile.id])  # Change to the correct name if needed
        data = {
            'first_name': 'Updated',
            'last_name': 'User',
            'personnummer': '900101-1234'
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.first_name, 'Updated')

    def test_delete_profile(self):
        url = reverse('profile-detail', args=[self.profile.id])  # Change to the correct name if needed
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Profile.objects.filter(id=self.profile.id).exists())

    
