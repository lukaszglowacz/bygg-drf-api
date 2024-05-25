from django.test import TestCase
from django.contrib.auth import get_user_model
from profiles.models import Profile
from workplace.models import Workplace
from .models import LiveSession

class LiveSessionModelTests(TestCase):

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
        self.live_session = LiveSession.objects.create(
            user=self.user,
            profile=self.profile,
            workplace=self.workplace
        )

    def test_live_session_creation(self):
        self.assertEqual(self.live_session.user, self.user)
        self.assertEqual(self.live_session.profile, self.profile)
        self.assertEqual(self.live_session.workplace, self.workplace)
        self.assertEqual(self.live_session.status, 'Trwa')

    def test_live_session_string_representation(self):
        expected_string = f"{self.user.email} - {self.live_session.start_time.strftime('%Y-%m-%d %H:%M')} - Trwa"
        self.assertEqual(str(self.live_session), expected_string)
