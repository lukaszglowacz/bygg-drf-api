from django.db import models
from profiles.models import Profile  # Importing the Profile model
from workplace.models import Workplace  # Importing the Workplace model
from django.core.exceptions import ValidationError

class WorkSession(models.Model):
    """
    Model to represent a work session, linking a user profile to a workplace with defined start and end times.
    """
    # ForeignKey relationship to Profile; deleting a profile will cascade and delete related work sessions
    profile = models.ForeignKey(
        Profile, 
        on_delete=models.CASCADE, 
        verbose_name="User profile"
    )
    
    # ForeignKey relationship to Workplace; deleting a workplace will cascade and delete related work sessions
    workplace = models.ForeignKey(
        Workplace, 
        on_delete=models.CASCADE, 
        verbose_name="Workplace"
    )
    
    # Date and time when the work session starts
    start_time = models.DateTimeField(verbose_name="Start time")
    
    # Date and time when the work session ends
    end_time = models.DateTimeField(verbose_name="End time")

    @property
    def total_time(self):
        """
        Computes the total duration of the work session in hours and minutes.
        """
        if self.start_time and self.end_time:
            delta = self.end_time - self.start_time  # Calculate time difference
            hours = delta.seconds // 3600  # Convert total seconds to hours
            minutes = (delta.seconds % 3600) // 60  # Remaining seconds converted to minutes
            return f"{hours} h, {minutes} min"  # Return formatted string

    def __str__(self):
        """
        Returns a string representation of the work session, showing the user's email and workplace address.
        """
        # Formatted string that includes the user's email and the full address of the workplace
        return f"{self.profile.user.email} - {self.workplace.street} {self.workplace.street_number}, {self.workplace.postal_code} {self.workplace.city}"

    def clean(self):
        """
        Custom validation to check that end_time is not earlier than start_time.
        """
        if self.end_time < self.start_time:
            raise ValidationError('End time cannot be earlier than start time.')