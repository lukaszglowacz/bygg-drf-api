from rest_framework import serializers
from .models import LiveSession  # Importing the LiveSession model
from profiles.models import Profile  # Importing the Profile model
from workplace.models import Workplace  # Importing the Workplace model
from profiles.serializers import ProfileSerializer  # Importing serializer for the Profile model
from workplace.serializers import WorkplaceSerializer  # Importing serializer for the Workplace model

class LiveSessionSerializer(serializers.ModelSerializer):
    # Linking profile and workplace fields to their respective models via primary key relationships
    profile = serializers.PrimaryKeyRelatedField(queryset=Profile.objects.all())
    workplace = serializers.PrimaryKeyRelatedField(queryset=Workplace.objects.all())
    # Customizing the datetime format for the start_time field
    start_time = serializers.DateTimeField(format='%Y.%m.%d %H:%M', required=False)

    class Meta:
        model = LiveSession  # Specifies the model associated with the serializer
        fields = [
            'id', 'profile', 'workplace', 'start_time', 'status'
        ]
        
    def create(self, validated_data):
        # Create method to instantiate a LiveSession object using validated data
        return LiveSession.objects.create(**validated_data)

    def to_representation(self, instance):
        # Customizing the output of the serialized data to include full profile and workplace data
        representation = super().to_representation(instance)
        representation['profile'] = ProfileSerializer(instance.profile).data
        representation['workplace'] = WorkplaceSerializer(instance.workplace).data
        return representation
