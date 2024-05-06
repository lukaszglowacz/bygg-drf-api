from django.db import models
from profiles.models import Profile
from livesession.models import LiveSession
from worksession.models import WorkSession
from django.db.models import Sum, F, ExpressionWrapper, fields
from datetime import timedelta


class Employee(models.Model):
    profile = models.OneToOneField(
        Profile, 
        on_delete=models.CASCADE,
        related_name='employee'
    )

    def __str__(self):
        return f"{self.profile.user.first_name} {self.profile.user.last_name} - {self.current_work_location}"
    
    