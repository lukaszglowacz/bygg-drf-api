from django.db import models
from profiles.models import Profile
from workplace.models import Workplace

class WorkSession(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name="Profil użytkownika")
    workplace = models.ForeignKey(Workplace, on_delete=models.CASCADE, verbose_name="Miejsce pracy")
    start_time = models.DateTimeField(verbose_name="Czas rozpoczęcia")
    end_time = models.DateTimeField(verbose_name="Czas zakończenia")

    @property
    def total_time(self):
        if self.start_time and self.end_time:
            delta = self.end_time - self.start_time
            hours = delta.seconds // 3600
            minutes = (delta.seconds % 3600) // 60
            return f"{hours} h, {minutes} min"

    def __str__(self):
        return f"{self.profile.user.email} - {self.workplace.street} {self.workplace.street_number}, {self.workplace.postal_code} {self.workplace.city}"
