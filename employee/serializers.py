from rest_framework import serializers
from .models import Employee
from profiles.models import Profile
from livesession.models import LiveSession
from workplace.serializers import WorkplaceSerializer



class ProfileWithEmployeeSerializer(serializers.ModelSerializer):
    current_session_start_time = serializers.SerializerMethodField()
    current_session_status = serializers.SerializerMethodField()
    current_workplace = serializers.SerializerMethodField()
    user_email = serializers.SerializerMethodField() 


    class Meta:
        model = Profile
        fields = ['id', 'full_name', 'user_email', 'personnummer', 'current_session_start_time', 'current_session_status', 'current_workplace', 'image']

    def get_current_session_start_time(self, profile):
        # Pobiera najnowszą sesję zgodnie z profilem
        session = LiveSession.objects.filter(profile=profile).order_by('-start_time').first()
        return session.start_time.strftime('%Y.%m.%d %H:%M') if session else None

    def get_current_session_status(self, profile):
        # Pobiera status najnowszej sesji
        session = LiveSession.objects.filter(profile=profile).order_by('-start_time').first()
        return session.status if session else 'Nie pracuje'
    
    def get_current_workplace(self, profile):
        session = LiveSession.objects.filter(profile=profile).order_by('-start_time').first()
        if session and session.workplace:
            workplace = session.workplace
            # Tworzenie stringa zawierającego adres
            return f"{workplace.street} {workplace.street_number}, {workplace.city}"
        return "Brak miejsca pracy"
    
    def get_user_email(self, obj):
        # Assuming 'profile' is linked to 'Employee' and 'user' to 'Profile'
        return obj.user.email if obj and obj.user else None
    

