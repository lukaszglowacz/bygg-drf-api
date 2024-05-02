from django.db import models
from profiles.models import Profile
from livesession.models import LiveSession

class Employee(models.Model):
    profile = models.OneToOneField(
        Profile, 
        on_delete=models.CASCADE,
        related_name='employee'
    )

    def __str__(self):
        return f"{self.profile.user.first_name} {self.profile.user.last_name} - {self.current_work_location}"
    
    @property
    def current_session_start_time(self):
        session = LiveSession.objects.filter(profile=self.profile, status='Trwa').first()
        return session.start_time if session else None

    @property
    def current_session_status(self):
        session = LiveSession.objects.filter(profile=self.profile, status='Trwa').first()
        return session.status if session else 'Brak sesji'