from django.db import models
from django.conf import settings
from workplace.models import Workplace

class LiveSession(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    workplace = models.ForeignKey(Workplace, on_delete=models.CASCADE)
    start_time = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=15, default='Trwa')
    
    def __str__(self):
        # Zakładam, że profil użytkownika jest dostępny przez related_name='profile'
        user_profile = self.user.profile
        first_name = user_profile.first_name
        last_name = user_profile.last_name
        return f"{first_name} {last_name} - {self.start_time.strftime('%Y-%m-%d %H:%M')} - {self.status}"
    