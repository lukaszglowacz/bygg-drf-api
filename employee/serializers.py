from rest_framework import serializers
from .models import Employee
from profiles.models import Profile
from livesession.models import LiveSession
from workplace.serializers import WorkplaceSerializer
from django.utils import timezone
from datetime import timedelta
from worksession.models import WorkSession
from django.db.models import Sum, F, ExpressionWrapper, fields
from django.db.models.functions import Cast



class ProfileWithEmployeeSerializer(serializers.ModelSerializer):
    current_session_start_time = serializers.SerializerMethodField()
    current_session_status = serializers.SerializerMethodField()
    current_workplace = serializers.SerializerMethodField()
    user_email = serializers.SerializerMethodField()
    work_session = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ['id', 'full_name', 'user_email', 'personnummer', 'current_session_start_time', 'current_session_status', 'current_workplace', 'image', 'work_session']

    def get_current_session_start_time(self, profile):
        session = LiveSession.objects.filter(profile=profile).order_by('-start_time').first()
        return session.start_time.strftime('%Y.%m.%d %H:%M') if session else None

    def get_current_session_status(self, profile):
        session = LiveSession.objects.filter(profile=profile).order_by('-start_time').first()
        return session.status if session else 'Nie pracuje'
    
    def get_current_workplace(self, profile):
        session = LiveSession.objects.filter(profile=profile).order_by('-start_time').first()
        if session and session.workplace:
            return f"{session.workplace.street} {session.workplace.street_number}, {session.workplace.city}"
        return "No job"
    
    def get_user_email(self, obj):
        return obj.user.email if obj and obj.user else None
    
    def get_work_session(self, obj):
        sessions = WorkSession.objects.filter(profile=obj).annotate(
            duration=ExpressionWrapper(F('end_time') - F('start_time'), output_field=fields.DurationField())
        ).values(
            'workplace__street', 
            'workplace__street_number', 
            'workplace__postal_code', 
            'workplace__city', 
            'start_time', 
            'end_time',
            'duration'
        )

        results = []
        for session in sessions:
            duration = session['duration']
            hours, remainder = divmod(duration.total_seconds(), 3600)
            minutes = (remainder % 3600) // 60
            formatted_duration = f"{int(hours)} h, {int(minutes)} min"

            results.append({
                "workplace": f"{session['workplace__street']} {session['workplace__street_number']}, {session['workplace__postal_code']} {session['workplace__city']}",
                "start_time": session['start_time'].strftime('%Y.%m.%d %H:%M'),
                "end_time": session['end_time'].strftime('%Y.%m.%d %H:%M'),
                "total_time": formatted_duration
            })
    
        return results