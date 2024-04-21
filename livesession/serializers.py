from rest_framework import serializers
from .models import LiveSession
from profiles.models import Profile
from workplace.models import Workplace
from profiles.serializers import ProfileSerializer
from workplace.serializers import WorkplaceSerializer

class LiveSessionSerializer(serializers.ModelSerializer):
    profile = serializers.PrimaryKeyRelatedField(queryset=Profile.objects.all())
    workplace = serializers.PrimaryKeyRelatedField(queryset=Workplace.objects.all())
    start_time = serializers.DateTimeField(format='%Y.%m.%d %H:%M', required=False)

    class Meta:
        model = LiveSession
        fields = [
            'id', 'profile', 'workplace', 'start_time', 'status'
        ]
        
    def create(self, validated_data):
        # Upewnij się, że wszystkie przekazane klucze są obsługiwane przez model
        return LiveSession.objects.create(**validated_data)

    def to_representation(self, instance):
        # Dostosowanie reprezentacji, aby zwracała pełne dane profilu i miejsca pracy
        representation = super().to_representation(instance)
        representation['profile'] = ProfileSerializer(instance.profile).data
        representation['workplace'] = WorkplaceSerializer(instance.workplace).data
        return representation
