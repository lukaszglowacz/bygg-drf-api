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
from django.db import transaction

class ProfileSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source='user.email', read_only=True)
    user_id = serializers.IntegerField(source='user.id', read_only=True)
    is_employer = serializers.BooleanField(source='user.is_employer', read_only=True)
    full_name = serializers.SerializerMethodField()

    created_at = serializers.DateTimeField(format='iso-8601', read_only=True)
    updated_at = serializers.DateTimeField(format='iso-8601', read_only=True)

    class Meta:
        model = Profile
        fields = ['id', 'user_email', 'user_id', 'full_name', 'first_name', 'last_name', 'personnummer', 'created_at', 'updated_at', 'image', 'is_employer']
        read_only_fields = ['user']

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"

User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    email = serializers.CharField(required=True, validators=[EmailValidator(message="Invalid email format")])
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    first_name = serializers.CharField(write_only=True, required=True)
    last_name = serializers.CharField(write_only=True, required=True)
    personnummer = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = ('email', 'password', 'first_name', 'last_name', 'personnummer')

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already in use")
        return value

    def validate_password(self, value):
        regex_password = re.compile(r'^(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$')
        if not regex_password.match(value):
            raise serializers.ValidationError("Password must be at least 8 characters with uppercase, number, and special character"
)
        validate_password(value)
        return value

    def validate_personnummer(self, value):
        regex = RegexValidator(regex=r'^\d{6}-\d{4}$', message='Invalid personnummer format, expected: YYMMDD-XXXX'
)
        try:
            regex(value)
        except ValidationError:
            raise serializers.ValidationError("Invalid personnummer format, expected: YYMMDD-XXXX")
        if Profile.objects.filter(personnummer=value).exists():
            raise serializers.ValidationError("Personnummer already in use")
        return value

    @transaction.atomic
    def create(self, validated_data):
        user = CustomUser(
            email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()

        Profile.objects.create(
            user=user,
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            personnummer=validated_data['personnummer']
        )
        return user

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(username=email, password=password)
        if not user:
            if not User.objects.filter(email=email).exists():
                raise serializers.ValidationError({'email': _('Email not found')})
            else:
                raise serializers.ValidationError({'password': _('Incorrect password')})

        data = super().validate(attrs)
        data['user_id'] = user.id
        
        if hasattr(user, 'profile'):
            data['profile_id'] = user.profile.id
        else:
            data['profile_id'] = None
            
        return data

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
