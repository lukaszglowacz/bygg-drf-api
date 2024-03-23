from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from datetime import timedelta

class WorkSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    workplace = models.ForeignKey('workplace.WorkPlace', on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    total_time = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, validators=[MinValueValidator(0)])

    def save(self, *args, **kwargs):
        if self.start_time and self.end_time:
            delta = self.end_time - self.start_time
            #Obliczanie calkowitego czasu pracy w godzinach z dokladnoscia do 2 miejsc po przecinku
            hours = delta.total_seconds() / 3600
            self.total_time = round(hours, 2)
        super(WorkSession, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.workplace.name} - {self.start_time.strftime('%Y-%m-%d %H:%M')}"