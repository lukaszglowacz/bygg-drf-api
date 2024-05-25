from worksession.models import WorkSession
from workplace.models import Workplace
from django.utils import timezone
from datetime import timedelta
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth import get_user_model
from profiles.models import Profile
from employee.models import Employee

class EmployeeAPITests(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user_model = get_user_model()
        
        # Creating a user and profile for the employer
        self.employer_user = self.user_model.objects.create_user(
            email='testemployer@example.com',
            password='Testpassword123!',
            is_employer=True
        )
        self.employer_profile = Profile.objects.create(
            user=self.employer_user,
            first_name='Employer',
            last_name='Test',
            personnummer='900101-1234'
        )
        self.employer_employee = Employee.objects.create(profile=self.employer_profile)

        # Creating another user and profile for the employee
        self.employee_user = self.user_model.objects.create_user(
            email='testemployee@example.com',
            password='Testpassword123!',
            is_employer=False
        )
        self.employee_profile = Profile.objects.create(
            user=self.employee_user,
            first_name='Employee',
            last_name='Test',
            personnummer='800101-1234'
        )
        self.employee = Employee.objects.create(profile=self.employee_profile)

        self.client.force_authenticate(user=self.employer_user)

    def test_list_employees(self):
        url = reverse('employee-list')
        response = self.client.get(url, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['full_name'], 'Employer Test')
        self.assertEqual(response.data[1]['full_name'], 'Employee Test')

    def test_retrieve_employee(self):
        url = reverse('employee-detail', kwargs={'pk': self.employee_profile.id})
        response = self.client.get(url, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['full_name'], 'Employee Test')
        self.assertEqual(response.data['personnummer'], '800101-1234')

    def test_delete_employee(self):
        url = reverse('employee-detail', kwargs={'pk': self.employee_profile.id})
        response = self.client.delete(url, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Employee.objects.count(), 1)

    def test_list_employees_with_work_sessions_filter(self):
        # Create work sessions for the filter test
        workplace = Workplace.objects.create(
            street='Test Street',
            street_number='123',
            postal_code='123 45',
            city='Test City'
        )

        WorkSession.objects.create(
            profile=self.employee_profile,
            workplace=workplace,
            start_time=timezone.now() - timedelta(days=10),
            end_time=timezone.now() - timedelta(days=9)
        )

        url = reverse('employee-detail', kwargs={'pk': self.employee_profile.id})
        response = self.client.get(url, {'year': timezone.now().year, 'month': timezone.now().month}, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['work_session']), 1)
