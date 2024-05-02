from rest_framework import serializers
from .models import Employee
from profiles.models import Profile
from livesession.models import LiveSession


class ProfileWithEmployeeSerializer(serializers.ModelSerializer):
    current_session_start_time = serializers.SerializerMethodField()
    current_session_status = serializers.SerializerMethodField()


    class Meta:
        model = Profile
        fields = ['id', 'full_name', 'personnummer', 'current_session_start_time', 'current_session_status']

    def get_current_session_start_time(self, profile):
        # Pobiera najnowszą sesję zgodnie z profilem
        session = LiveSession.objects.filter(profile=profile).order_by('-start_time').first()
        return session.start_time.strftime('%Y.%m.%d %H:%M') if session else None

    def get_current_session_status(self, profile):
        # Pobiera status najnowszej sesji
        session = LiveSession.objects.filter(profile=profile).order_by('-start_time').first()
        return session.status if session else 'Brak sesji'