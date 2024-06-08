import re  # Importing the regex module to use for password validation
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.password_validation import validate_password  # Importing Django's built-in password validator
from rest_framework import serializers  # Importing serializers from Django REST Framework
from .models import CustomUser  # Importing the CustomUser model from the local models module

# UserSerializer class to serialize and deserialize the CustomUser instances
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser  # Specifies the model to serialize
        fields = ['email', 'password', 'is_employer']  # Fields to include in the serialization/deserialization
        extra_kwargs = {
            'email': {
                'required': True,
                'error_messages': {
                    'blank': 'Email is required',  # Custom error message for empty email field
                }
            },
            'password': {
                'write_only': True,  # Password should not be read back
                'required': True,
                'error_messages': {
                    'blank': 'Password is required.',  # Custom error message for empty password field
                    'required': 'This field is required'  # Optional additional message
                }
            }
        }

    # Custom validation for the 'password' field
    def validate_password(self, value):
        # Regular expression for validating a password
        regex_password = re.compile(r'^(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$')

        # Check if the password matches the regex pattern
        if not regex_password.match(value):
            raise serializers.ValidationError(
                "Password must be at least 8 characters, including 1 uppercase letter, 1 number, and 1 special character"
            )

        # Additional password validation using Django's built-in tools
        validate_password(value)
        return value

    # Create a new user instance from validated data
    def create(self, validated_data):
        user = CustomUser(
            email=validated_data['email'],
            is_employer=validated_data.get('is_employer', False)  # Set 'is_employer' flag from data, default to False
        )
        user.set_password(validated_data['password'])  # Securely set user password
        user.save()  # Save the user instance to the database
        return user
