from django.test import TestCase
from django.utils.timezone import now, timedelta
from django.contrib.auth import get_user_model
from .models import WorkSession
from profiles.models import Profile
from workplace.models import Workplace
from django.core.exceptions import ValidationError

class WorkSessionModelTests(TestCase):

    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(
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
            start_time=now(),
            end_time=now() + timedelta(hours=1)
        )

    def test_work_session_creation(self):
        self.assertEqual(self.work_session.profile, self.profile)
        self.assertEqual(self.work_session.workplace, self.workplace)
        self.assertEqual(self.work_session.total_time, '1 h, 0 min')
        self.assertEqual(
            str(self.work_session),
            f'{self.profile.user.email} - {self.workplace.street} {self.workplace.street_number}, {self.workplace.postal_code} {self.workplace.city}'
        )

    def test_invalid_end_time(self):
        work_session = WorkSession(
            profile=self.profile,
            workplace=self.workplace,
            start_time=now(),
            end_time=now() - timedelta(hours=1)
        )
        with self.assertRaises(ValidationError):
            work_session.full_clean()  # This will trigger the validation

