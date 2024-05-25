from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth import get_user_model
from profiles.models import Profile
from workplace.models import Workplace
from .models import WorkSession
from django.utils import timezone
from datetime import timedelta

class WorkSessionAPITests(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user_model = get_user_model()
        
        # Creating a user and profile
        self.user = self.user_model.objects.create_user(
            email='testuser@example.com',
            password='Testpassword123!'
        )
        self.profile = Profile.objects.create(
            user=self.user,
            first_name='John',
            last_name='Doe',
            personnummer='900101-1234'
        )
        self.workplace = Workplace.objects.create(
            street='Main',
            street_number='123',
            postal_code='123 45',
            city='Sample City'
        )
        self.work_session = WorkSession.objects.create(
            profile=self.profile,
            workplace=self.workplace,
            start_time=timezone.now(),
            end_time=timezone.now() + timedelta(hours=1)
        )
        self.client.force_authenticate(user=self.user)

    def test_list_work_sessions(self):
        url = reverse('worksession-list')
        response = self.client.get(url, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['profile']['id'], self.profile.id)
        self.assertEqual(response.data[0]['workplace']['id'], self.workplace.id)

    def test_create_work_session(self):
        url = reverse('worksession-list')
        data = {
            'profile': self.profile.id,
            'workplace': self.workplace.id,
            'start_time': timezone.now(),
            'end_time': timezone.now() + timedelta(hours=2)
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(WorkSession.objects.count(), 2)

    def test_retrieve_work_session(self):
        url = reverse('worksession-detail', kwargs={'pk': self.work_session.id})
        response = self.client.get(url, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['profile']['id'], self.profile.id)
        self.assertEqual(response.data['workplace']['id'], self.workplace.id)

    def test_update_work_session(self):
        url = reverse('worksession-detail', kwargs={'pk': self.work_session.id})
        new_workplace = Workplace.objects.create(
            street='Second',
            street_number='456',
            postal_code='678 90',
            city='New City'
        )
        data = {
            'profile': self.profile.id,
            'workplace': new_workplace.id,
            'start_time': timezone.now(),
            'end_time': timezone.now() + timedelta(hours=3)
        }
        response = self.client.put(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.work_session.refresh_from_db()
        self.assertEqual(self.work_session.workplace, new_workplace)

    def test_delete_work_session(self):
        url = reverse('worksession-detail', kwargs={'pk': self.work_session.id})
        response = self.client.delete(url, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(WorkSession.objects.count(), 0)
