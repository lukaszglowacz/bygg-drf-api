from django.db import models
from django.core.exceptions import ValidationError
from django.conf import settings
from workplace.models import Workplace
from django.utils import timezone

class WorkSession(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    workplace = models.ForeignKey(Workplace, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True, blank=True)
    
    @property
    def total_time(self):
        if self.start_time and self.end_time:
            delta = self.end_time - self.start_time
            return round(delta.total_seconds() / 3600, 2)
        elif self.start_time and not self.end_time:
            delta = timezone.now() - self.start_time
            return round(delta.total_seconds() / 3600, 2)
        return None

    def clean(self):
        if self.end_time and self.end_time < self.start_time:
            raise ValidationError('Czas zakończenia nie może być wcześniejszy niż czas rozpoczęcia')
        
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user} - {self.workplace.street} {self.workplace.street_number}, {self.workplace.postal_code} {self.workplace.city} - {self.start_time.strftime('%Y-%m-%d %H:%M')}"

