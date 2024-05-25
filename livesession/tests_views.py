from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth import get_user_model
from profiles.models import Profile
from workplace.models import Workplace
from worksession.models import WorkSession
from .models import LiveSession

class LiveSessionAPITests(APITestCase):

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
        self.workplace = Workplace.objects.create(
            street='Main',
            street_number='123',
            postal_code='123 45',
            city='Sample City'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_start_live_session(self):
        url = reverse('start-live-session')  # Change to the correct name if needed
        data = {
            'profile': self.profile.id,
            'workplace': self.workplace.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(LiveSession.objects.count(), 1)
        self.assertEqual(LiveSession.objects.get().status, 'Trwa')

    def test_end_live_session(self):
        live_session = LiveSession.objects.create(
            user=self.user,
            profile=self.profile,
            workplace=self.workplace
        )
        url = reverse('end-live-session', args=[live_session.id])  # Change to the correct name if needed
        response = self.client.patch(url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(LiveSession.objects.count(), 0)
        self.assertEqual(WorkSession.objects.count(), 1)
        self.assertEqual(WorkSession.objects.get().profile, self.profile)

    def test_active_live_sessions(self):
        LiveSession.objects.create(
            user=self.user,
            profile=self.profile,
            workplace=self.workplace
        )
        url = reverse('active-live-sessions')  # Change to the correct name if needed
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
