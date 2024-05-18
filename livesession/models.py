from django.db import models
from profiles.models import Profile
from workplace.models import Workplace
from django.conf import settings

class LiveSession(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,null=True, on_delete=models.CASCADE, verbose_name="User")
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name="User profile")
    workplace = models.ForeignKey(Workplace, on_delete=models.CASCADE, verbose_name="Workplace")
    start_time = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=15, default='Trwa')

    def __str__(self):
        return f"{self.user.email} - {self.start_time.strftime('%Y-%m-%d %H:%M')} - {self.status}"
