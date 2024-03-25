from django.test import TestCase
from django.contrib.auth import get_user_model
from .serializers import UserRegistrationSerializer
from .models import Profile


class UserRegistrationSerializerTest(TestCase):
    def test_user_registration(self):
        user_data = {
            "email": "user@example.com",
            "password": "TwojeHaslo123",
            "first_name": "Jan",
            "last_name": "Kowalski",
            "personnummer": "123456-7890"
        }
        
        serializer = UserRegistrationSerializer(data=user_data)
        valid = serializer.is_valid()
        if not valid:
            print(serializer.errors)  # Dodano wypisanie błędów
        self.assertTrue(valid)
        
        user = serializer.save()
        self.assertIsNotNone(user.id)
        self.assertEqual(user.email, "user@example.com")
        # Dodaj więcej asercji według potrzeb



User = get_user_model()

class UserProfileTest(TestCase):
    def test_user_profile_creation(self):
        user_data = {
            "email": "test@example.com",
            "password": "securepassword123",
            "first_name": "Test",
            "last_name": "User",
            "personnummer": "123456-7890"
        }
        user = User.objects.create_user(**user_data)
        self.assertIsNotNone(user.id, "Failed to create user")
        
        # Sprawdzenie, czy profil został utworzony
        profile_exists = Profile.objects.filter(user=user).exists()
        self.assertTrue(profile_exists, "Profile was not created for the user")
        
        # Sprawdzenie czy dane profilu są prawidłowe
        profile = Profile.objects.get(user=user)
        self.assertEqual(profile.first_name, user_data['first_name'], "Profile first name does not match")
        self.assertEqual(profile.last_name, user_data['last_name'], "Profile last name does not match")
        self.assertEqual(profile.personnummer, user_data['personnummer'], "Profile personnummer does not match")
