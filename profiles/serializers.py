from rest_framework import serializers
from .models import Profile
from django.contrib.auth import authenticate, get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.core.validators import RegexValidator, EmailValidator
from django.core.exceptions import ValidationError
from accounts.models import CustomUser
from django.contrib.auth.password_validation import validate_password
import re
from django.utils.translation import gettext_lazy as _




class ProfileSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source='user.email', read_only=True)
    user_id = serializers.IntegerField(source='user.id', read_only=True)
    full_name = serializers.SerializerMethodField()

    # Formatowanie pól daty/godziny
    created_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M', read_only=True)
    updated_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M', read_only=True)

    class Meta:
        model = Profile
        fields = [
            'id',
            'user_email',
            'user_id', 
            'full_name',
            'first_name',
            'last_name',
            'personnummer',
            'created_at', 
            'updated_at',
            'image'
        ]
        read_only_fields = ['user']

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    
User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    email = serializers.CharField(
        required=True,
        validators=[EmailValidator(message="Invalid email address format.")],
        error_messages={
            'blank': 'E-mail is required.',
            'required': 'This field is mandatory.'
        }
    )
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'},
        error_messages={
            'blank': 'Password is required.',
            'required': 'This field is mandatory.'
        }
    )
    first_name = serializers.CharField(
        write_only=True,
        required=True,
        error_messages={'blank': 'This field cannot be empty.'}
    )
    last_name = serializers.CharField(
        write_only=True,
        required=True,
        error_messages={'blank': 'This field cannot be empty.'}
    )
    personnummer = serializers.CharField(
        write_only=True,
        required=True,
        error_messages={'blank': 'This field cannot be empty.'}
    )

    class Meta:
        model = CustomUser
        fields = ('email', 'password', 'first_name', 'last_name', 'personnummer')
        extra_kwargs = {
            'email': {'required': True, 'error_messages': {'blank': 'The field is required.', 'required': 'The field is required.'}},
            'password': {'write_only': True, 'required': True, 'error_messages': {'blank': 'The field is required.', 'required': 'The field is required.'}},
            'first_name': {'required': True, 'error_messages': {'blank': 'The field is required.', 'required': 'The field is required.'}},
            'last_name': {'required': True, 'error_messages': {'blank': 'The field is required.', 'required': 'The field is required.'}},
            'personnummer': {'required': True, 'error_messages': {'blank': 'The field is required.', 'required': 'The field is required.'}}
        }
        
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email address is already in use. Please use a different address.")
        return value
        
    def validate_password(self, value):
        # Określenie wzorca regex dla hasła
        regex_password = re.compile(r'^(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$')

        # Sprawdzenie regex dla hasła
        if not regex_password.match(value):
            raise serializers.ValidationError(
                "The password must contain at least 8 characters, one uppercase letter, one number and one special character."
            )

        # Dodatkowa walidacja hasła za pomocą wbudowanych narzędzi Django
        validate_password(value)
        return value
    
    


    def validate_personnummer(self, value):
        regex = RegexValidator(regex=r'^\d{6}-\d{4}$', message='Expected personnummer format: YYMMDD-XXXX.')
        try:
            regex(value)
        except ValidationError:
            raise serializers.ValidationError("Invalid personnummer format. Expected format: YYMMDD-XXXX.")
        if Profile.objects.filter(personnummer=value).exists():
            raise serializers.ValidationError("This personnumber is already in use. Please use another number.")
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
        # Custom validations
        email = attrs.get('email')
        password = attrs.get('password')

        # Validate email presence and format
        if not email:
            raise serializers.ValidationError({'email': _('E-mail is required.')})
        if '@' not in email:
            raise serializers.ValidationError({'email': _('Enter a valid email address with the "@" sign.')})

        # Authenticate user
        user = authenticate(username=email, password=password)
        if not user:
            # If user does not exist or password is incorrect
            if not User.objects.filter(email=email).exists():
                raise serializers.ValidationError({'email': _('No user found with this email address.')})
            else:
                raise serializers.ValidationError({'password': _('Invalid password.')})

        # If authentication succeeds, proceed with the default JWT token creation
        data = super().validate(attrs)
        data['user_id'] = user.id  # Include user ID in the token response
        
        if hasattr(user, 'profile'):
            data['profile_id'] = user.profile.id
        else:
            data['profile_id'] = None
            
        return data


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


