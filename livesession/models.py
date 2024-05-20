from django.db import models
from profiles.models import Profile  # Importing the Profile model which is related to User
from workplace.models import Workplace  # Importing the Workplace model to link sessions to a workplace
from django.conf import settings  # Importing Django settings to reference the auth user model

class LiveSession(models.Model):
    # Linking to the custom user model specified in Django settings; allows deletion of the user without deleting the session
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        null=True,  # Allows this field to be null in the database
        on_delete=models.CASCADE,  # Deletes the session if the related user is deleted
        verbose_name="User"
    )

    # Link to a profile, deleting this will also delete the session
    profile = models.ForeignKey(
        Profile, 
        on_delete=models.CASCADE, 
        verbose_name="User profile"
    )

    # Link to a workplace, deleting the workplace will delete the session
    workplace = models.ForeignKey(
        Workplace, 
        on_delete=models.CASCADE, 
        verbose_name="Workplace"
    )

    # Automatically set the start time to the current time when a session is created
    start_time = models.DateTimeField(
        auto_now_add=True  # Automatically set to now when the object is first created
    )

    # Status field with a default value
    status = models.CharField(
        max_length=15, 
        default='Trwa'  # Default status indicating the session is ongoing ('Trwa' means 'Ongoing' in Polish)
    )

    def __str__(self):
        # Return a string representation of the session including the user's email, start time, and status
        return f"{self.user.email} - {self.start_time.strftime('%Y-%m-%d %H:%M')} - {self.status}"
