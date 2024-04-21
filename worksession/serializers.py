from rest_framework import serializers
from .models import WorkSession, Profile, Workplace

class SimpleProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'full_name', 'personnummer']

class SimpleWorkplaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workplace
        fields = ['id', 'street', 'street_number', 'postal_code', 'city']

class WorkSessionSerializer(serializers.ModelSerializer):
    profile = serializers.PrimaryKeyRelatedField(queryset=Profile.objects.all())
    workplace = serializers.PrimaryKeyRelatedField(queryset=Workplace.objects.all())
    start_time = serializers.DateTimeField(format='%Y.%m.%d %H:%M')
    end_time = serializers.DateTimeField(format='%Y.%m.%d %H:%M')
    total_time = serializers.ReadOnlyField()  # Oznaczone jako tylko do odczytu, ponieważ jest obliczane

    class Meta:
        model = WorkSession
        fields = ['id', 'profile', 'workplace', 'start_time', 'end_time', 'total_time']

    def validate(self, data):
        if 'end_time' in data and data.get('end_time') < data['start_time']:
            raise serializers.ValidationError("Czas zakończenia nie może być wcześniejszy niż czas rozpoczęcia")
        return data

    def to_representation(self, instance):
        """Modify the representation of `start_time` and `end_time` to 'RR.MM.DD HH:MM' format."""
        representation = super().to_representation(instance)
        representation['profile'] = SimpleProfileSerializer(instance.profile).data
        representation['workplace'] = SimpleWorkplaceSerializer(instance.workplace).data
        representation['start_time'] = instance.start_time.strftime('%y.%m.%d %H:%M')
        representation['end_time'] = instance.end_time.strftime('%y.%m.%d %H:%M')
        return representation
