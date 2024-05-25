from django.test import TestCase
from django.contrib.auth import get_user_model
from profiles.models import Profile
from livesession.models import LiveSession
from workplace.models import Workplace
from worksession.models import WorkSession
from .models import Employee
from .serializers import ProfileWithEmployeeSerializer
from datetime import datetime, timedelta
from django.utils import timezone

class EmployeeModelTests(TestCase):

    def setUp(self):
        self.user_model = get_user_model()
        self.user = self.user_model.objects.create_user(
            email='testuser@example.com',
            password='Testpassword123!',
            first_name='John',
            last_name='Doe',
            is_employer=False
        )
        self.profile = Profile.objects.create(
            user=self.user,
            first_name='John',
            last_name='Doe',
            personnummer='900101-1234'
        )
        self.employee = Employee.objects.create(profile=self.profile)

    def test_employee_creation(self):
        # Test if the employee is correctly created
        self.assertEqual(self.employee.profile, self.profile)

    def test_employee_string_representation(self):
        # Test if the string representation is correct
        self.assertEqual(str(self.employee), 'John Doe')


class ProfileWithEmployeeSerializerTests(TestCase):

    def setUp(self):
        self.user_model = get_user_model()
        self.user = self.user_model.objects.create_user(
            email='testuser@example.com',
            password='Testpassword123!',
            first_name='John',
            last_name='Doe',
            is_employer=False
        )
        self.profile = Profile.objects.create(
            user=self.user,
            first_name='John',
            last_name='Doe',
            personnummer='900101-1234'
        )
        self.employee = Employee.objects.create(profile=self.profile)

        self.workplace = Workplace.objects.create(
            street='Test Street',
            street_number='123',
            postal_code='123 45',
            city='Test City'
        )

        self.live_session = LiveSession.objects.create(
            user=self.user,
            profile=self.profile,
            workplace=self.workplace,
            start_time=timezone.now() - timedelta(hours=1),
            status='Trwa'
        )

        self.work_session = WorkSession.objects.create(
            profile=self.profile,
            workplace=self.workplace,
            start_time=timezone.now() - timedelta(hours=2),
            end_time=timezone.now() - timedelta(hours=1)
        )

    def test_serializer_data(self):
        serializer = ProfileWithEmployeeSerializer(self.profile)
        data = serializer.data

        self.assertEqual(data['full_name'], 'John Doe')
        self.assertEqual(data['user_email'], 'testuser@example.com')
        self.assertEqual(data['personnummer'], '900101-1234')
        self.assertEqual(data['current_session_status'], 'Trwa')
        self.assertEqual(data['current_workplace'], 'Test Street 123, Test City')
        self.assertEqual(data['work_session'][0]['total_time'], '1 h, 0 min')

    def test_serializer_no_current_session(self):
        self.live_session.delete()
        serializer = ProfileWithEmployeeSerializer(self.profile)
        data = serializer.data

        self.assertEqual(data['current_session_status'], 'Nie pracuje')
        self.assertEqual(data['current_workplace'], 'No job')
