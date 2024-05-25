from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Profile
from django.core.exceptions import ValidationError

class ProfileModelTests(TestCase):

    def setUp(self):
        self.user_model = get_user_model()
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

    def test_profile_creation(self):
        self.assertEqual(self.profile.user, self.user)
        self.assertEqual(self.profile.first_name, 'John')
        self.assertEqual(self.profile.last_name, 'Doe')
        self.assertEqual(self.profile.personnummer, '900101-1234')
        self.assertEqual(str(self.profile), 'John Doe')

    def test_full_name_property(self):
        self.assertEqual(self.profile.full_name, 'John Doe')

    def test_invalid_personnummer(self):
        with self.assertRaises(ValidationError):
            profile = Profile(
                user=self.user,
                first_name='Jane',
                last_name='Doe',
                personnummer='invalid'
            )
            profile.full_clean()

    def test_duplicate_personnummer(self):
        with self.assertRaises(Exception):
            Profile.objects.create(
                user=self.user_model.objects.create_user(email='newuser@example.com', password='Testpassword123!'),
                first_name='Jane',
                last_name='Doe',
                personnummer='900101-1234'
            )
