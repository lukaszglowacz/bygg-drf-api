from django.test import TestCase
from django.contrib.auth import get_user_model

class CustomUserTests(TestCase):

    def setUp(self):
        self.user_model = get_user_model()

    def test_create_user(self):
        user = self.user_model.objects.create_user(
            email='testuser@example.com',
            password='Testpassword123!',
            is_employer=False
        )
        self.assertEqual(user.email, 'testuser@example.com')
        self.assertTrue(user.check_password('Testpassword123!'))
        self.assertFalse(user.is_employer)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        admin_user = self.user_model.objects.create_superuser(
            email='admin@example.com',
            password='Testpassword123!'
        )
        self.assertEqual(admin_user.email, 'admin@example.com')
        self.assertTrue(admin_user.check_password('Testpassword123!'))
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)

    def test_email_normalization(self):
        email = 'testuser@EXAMPLE.COM'
        user = self.user_model.objects.create_user(
            email=email,
            password='Testpassword123!'
        )
        self.assertEqual(user.email, email.lower())

    def test_invalid_email(self):
        with self.assertRaises(ValueError):
            self.user_model.objects.create_user(
                email='',
                password='Testpassword123!'
            )

    def test_duplicate_email(self):
        email = 'testuser@example.com'
        self.user_model.objects.create_user(
            email=email,
            password='Testpassword123!'
        )
        with self.assertRaises(Exception):
            self.user_model.objects.create_user(
                email=email,
                password='Testpassword123!'
            )
