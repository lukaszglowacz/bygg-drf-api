import re
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from .models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email', 'password', 'is_employer']
        extra_kwargs = {
            'email': {
                'required': True,
                'error_messages': {
                    'blank': 'Adres email jest wymagany.',  # Niestandardowy komunikat dla pustego pola
                }
            },
            'password': {
                'write_only': True,
                'required': True,
                'error_messages': {
                    'blank': 'Hasło jest wymagane.',  # Niestandardowy komunikat dla pustego pola
                    'required': 'To pole jest obowiązkowe.'  # Możesz użyć tego samego lub innego komunikatu
                }
            }
        }

    def validate_password(self, value):
        # Określenie wzorca regex dla hasła
        regex_password = re.compile(r'^(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$')

        # Sprawdzenie regex dla hasła
        if not regex_password.match(value):
            raise serializers.ValidationError(
                "Hasło musi zawierać co najmniej 8 znaków, jedną dużą literę, jedną cyfrę i jeden znak specjalny."
            )

        # Dodatkowa walidacja hasła za pomocą wbudowanych narzędzi Django
        validate_password(value)
        return value

    def create(self, validated_data):
        user = CustomUser(
            email=validated_data['email'],
            is_employer=validated_data.get('is_employer', False)
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

