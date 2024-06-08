from rest_framework import serializers
from .models import WorkSession, Profile, Workplace

class SimpleProfileSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source='user.email', read_only=True)
    
    class Meta:
        model = Profile
        fields = ['id', 'full_name', 'personnummer', 'image', 'user_email']

class SimpleWorkplaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workplace
        fields = ['id', 'street', 'street_number', 'postal_code', 'city']

class WorkSessionSerializer(serializers.ModelSerializer):
    profile = serializers.PrimaryKeyRelatedField(queryset=Profile.objects.all())
    workplace = serializers.PrimaryKeyRelatedField(queryset=Workplace.objects.all())
    
    start_time = serializers.DateTimeField(format='iso-8601')
    end_time = serializers.DateTimeField(format='iso-8601')
    
    total_time = serializers.ReadOnlyField()

    class Meta:
        model = WorkSession
        fields = ['id', 'profile', 'workplace', 'start_time', 'end_time', 'total_time']

    def validate(self, data):
        if 'end_time' in data and data.get('end_time') < data['start_time']:
            raise serializers.ValidationError("End time must be after start time")
        return data

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['profile'] = SimpleProfileSerializer(instance.profile).data
        representation['workplace'] = SimpleWorkplaceSerializer(instance.workplace).data
        return representation
