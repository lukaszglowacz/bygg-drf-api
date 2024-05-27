from rest_framework import serializers
import re
from django.contrib.auth.password_validation import validate_password as django_validate_password

class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True, required=True, min_length=8)
    confirm_password = serializers.CharField(write_only=True, required=True, min_length=8)

    def validate_password(self, value):
        # Password complexity validation
        regex_password = re.compile(r'^(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$')
        if not regex_password.match(value):
            raise serializers.ValidationError("The password must contain at least 8 characters, one uppercase letter, one number, and one special character.")
        django_validate_password(value)
        return value

    def validate(self, data):
        """
        Check that the two password entries match.
        """
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({"confirm_password": "Passwords do not match."})
        self.validate_password(data['password'])
        return data
