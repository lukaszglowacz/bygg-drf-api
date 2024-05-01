from django.db import models
from django.conf import settings

class Employee(models.Model):
    profile = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='employee'
    )
    total_hours_worked = models.PositiveIntegerField(default=0)
    current_work_location = models.CharField(max_length=100, blank=True)
    work_start_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.profile.first_name} {self.profile.last_name} - {self.current_work_location}"
