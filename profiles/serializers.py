from rest_framework import serializers
from .models import Profile
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


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
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    first_name = serializers.CharField(write_only=True, required=True)
    last_name = serializers.CharField(write_only=True, required=True)
    personnummer = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('email', 'password', 'first_name', 'last_name', 'personnummer')

    def validate_personnummer(self, value):
        print(f"Validating personnummer: {value}")  # Dodaj logowanie
        if Profile.objects.filter(personnummer=value).exists():
            raise serializers.ValidationError("Ten personnummer jest już używany.")
        return value

    def create(self, validated_data):
        # Tworzenie użytkownika
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password']
        )
        
        # Tworzenie profilu z dodatkowymi danymi
        Profile.objects.create(
            user=user,
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
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
