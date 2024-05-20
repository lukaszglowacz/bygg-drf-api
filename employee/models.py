from django.db import models
from profiles.models import Profile  # Importing the Profile model from the profiles app
from django.db.models import Sum, F, ExpressionWrapper, fields  # Importing database functions for complex queries
from datetime import timedelta  # Importing timedelta for handling time-related calculations

class Employee(models.Model):
    # A one-to-one link between Employee and Profile models, cascading on delete
    profile = models.OneToOneField(
        Profile, 
        on_delete=models.CASCADE,  # Ensures deletion of Employee instance if associated Profile is deleted
        related_name='employee'  # Allows access to this employee instance through the Profile model
    )

    def __str__(self):
        # String representation of the Employee model
        return f"{self.profile.user.first_name} {self.profile.user.last_name} - {self.current_work_location}"
