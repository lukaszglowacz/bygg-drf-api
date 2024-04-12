from rest_framework import serializers
from .models import Profile
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.core.validators import RegexValidator, EmailValidator
from django.core.exceptions import ValidationError
from accounts.models import CustomUser
from django.contrib.auth.password_validation import validate_password
import re



class ProfileSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source='user.email', read_only=True)
    user_id = serializers.IntegerField(source='user.id', read_only=True)

    # Formatowanie pól daty/godziny
    created_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M', read_only=True)
    updated_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M', read_only=True)

    class Meta:
        model = Profile
        fields = [
            'id',
            'user_email',
            'user_id', 
            'first_name',
            'last_name',
            'personnummer',
            'created_at', 
            'updated_at',
            'image'
        ]
        read_only_fields = ['user']


User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    email = serializers.CharField(
        required=True,
        validators=[EmailValidator(message="Nieprawidłowy format adresu email.")],
        error_messages={
            'blank': 'E-mail jest wymagany.',
            'required': 'To pole jest obowiązkowe.'
        }
    )
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'},
        error_messages={
            'blank': 'Hasło jest wymagane.',
            'required': 'To pole jest obowiązkowe.'
        }
    )
    first_name = serializers.CharField(
        write_only=True,
        required=True,
        error_messages={'blank': 'To pole nie może być puste.'}
    )
    last_name = serializers.CharField(
        write_only=True,
        required=True,
        error_messages={'blank': 'To pole nie może być puste.'}
    )
    personnummer = serializers.CharField(
        write_only=True,
        required=True,
        error_messages={'blank': 'To pole nie może być puste.'}
    )

    class Meta:
        model = CustomUser
        fields = ('email', 'password', 'first_name', 'last_name', 'personnummer')
        
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Ten adres email jest już używany. Proszę użyć innego adresu.")
        return value
        
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
    
    


    def validate_personnummer(self, value):
        regex = RegexValidator(regex=r'^\d{6}-\d{4}$', message='Oczekiwany format personnummer: XXXXXX-XXXX.')
        try:
            regex(value)
        except ValidationError:
            raise serializers.ValidationError("Niepoprawny format personnummer. Oczekiwany format: XXXXXX-XXXX.")
        if Profile.objects.filter(personnummer=value).exists():
            raise serializers.ValidationError("Ten personnummer jest już używany. Proszę użyć innego numeru.")
        return value
    
    def create(self, validated_data):
        user = CustomUser(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        user.set_password(validated_data['password'])
        user.save()

        Profile.objects.create(
            user=user,
            personnummer=validated_data['personnummer']
        )
        return user

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data['user_id'] = self.user.id
        return data


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
