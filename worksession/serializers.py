from rest_framework import serializers
from .models import WorkSession, Profile, Workplace
from profiles.serializers import ProfileSerializer
from workplace.serializers import WorkplaceSerializer

class WorkSessionSerializer(serializers.ModelSerializer):
    profile = serializers.PrimaryKeyRelatedField(queryset=Profile.objects.all(), required=False)
    workplace = serializers.PrimaryKeyRelatedField(queryset=Workplace.objects.all(), required=False)
    start_time = serializers.DateTimeField()
    end_time = serializers.DateTimeField()

    class Meta:
        model = WorkSession
        fields = ['id', 'profile', 'workplace', 'start_time', 'end_time', 'total_time']
        extra_kwargs = {'total_time': {'read_only': True}}

    def validate(self, data):
        if 'end_time' in data and data.get('end_time') and data['end_time'] < data['start_time']:
            raise serializers.ValidationError("Czas zakończenia nie może być wcześniejszy niż czas rozpoczęcia")
        return data

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['profile'] = ProfileSerializer(instance.profile).data
        representation['workplace'] = WorkplaceSerializer(instance.workplace).data
        return representation
