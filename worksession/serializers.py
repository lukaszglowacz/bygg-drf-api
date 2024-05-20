from rest_framework import serializers
from .models import WorkSession, Profile, Workplace

class SimpleProfileSerializer(serializers.ModelSerializer):
    # This field extracts the email from the associated user model, read-only.
    user_email = serializers.EmailField(source='user.email', read_only=True)
    
    class Meta:
        model = Profile
        fields = ['id', 'full_name', 'personnummer', 'image', 'user_email']

class SimpleWorkplaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workplace
        fields = ['id', 'street', 'street_number', 'postal_code', 'city']

class WorkSessionSerializer(serializers.ModelSerializer):
    # Links to Profile and Workplace using primary key related fields for efficient serialization.
    profile = serializers.PrimaryKeyRelatedField(queryset=Profile.objects.all())
    workplace = serializers.PrimaryKeyRelatedField(queryset=Workplace.objects.all())
    
    # Fields for managing start and end times of a work session.
    start_time = serializers.DateTimeField()
    end_time = serializers.DateTimeField()
    
    # A read-only field to display the total time calculated from the model's method.
    total_time = serializers.ReadOnlyField()

    class Meta:
        model = WorkSession
        fields = ['id', 'profile', 'workplace', 'start_time', 'end_time', 'total_time']

    def validate(self, data):
        # Custom validation to ensure that the end time is not earlier than the start time.
        if 'end_time' in data and data.get('end_time') < data['start_time']:
            raise serializers.ValidationError("The end time cannot be earlier than the start time")
        return data

    def to_representation(self, instance):
        """
        Custom representation of the serialized data to include nested representations
        of profile and workplace, and to format date times.
        """
        representation = super().to_representation(instance)
        # Use nested serializers to include details of profile and workplace in the response.
        representation['profile'] = SimpleProfileSerializer(instance.profile).data
        representation['workplace'] = SimpleWorkplaceSerializer(instance.workplace).data
        # Format datetime fields to a more readable format.
        representation['start_time'] = instance.start_time.strftime('%Y-%m-%d %H:%M')
        representation['end_time'] = instance.end_time.strftime('%Y-%m-%d %H:%M')
        return representation
