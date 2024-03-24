from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import RegexValidator
from workplace.models import Workplace
from worksession.models import WorkSession
from django.conf import settings

personnummer_regex = RegexValidator(regex=r'^\d{6}-\d{4}$', message='XXXXXX-XXXX')

class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    personnummer = models.CharField(max_length=11, unique=True, validators=[personnummer_regex])
    image = models.ImageField(upload_to='images/', default='../default_profile_l2i70s')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def total_work_hours(self):
        #Oblicza laczna ilosc godzin przepracowanych przez uzytkownika
        sessions = WorkSession.objects.filter(user=self.user)
        total_hours = sum(session.total_time for session in sessions if session.total_time)
        return total_hours
    
    def total_workplaces(self):
        #Zwraca liste unikalnych miejsc pracy, w ktorych przepracowal uzytkownik
        sessions = WorkSession.objects.filter(user=self.user).select_related('workplace')
        unique_workplaces = {session.workplace for session in sessions}
        return unique_workplaces

    def __str__(self):
        return self.user.username
    
