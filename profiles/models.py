from django.db import models
from django.core.validators import RegexValidator
from django.conf import settings
from .validators import validate_image_file_size, validate_image_dimensions  # Custom validators for the image field

# Regex validator for Swedish personal identity number 'personnummer'
personnummer_regex = RegexValidator(regex=r'^\d{6}-\d{4}$', message='RRMMDD-XXXX')

class Profile(models.Model):
    # Linking each profile uniquely to a user. Deletion of the user will also delete the profile.
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    # Fields for storing the first and last name, with a maximum character limit
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    # A unique personal number field with a specific format validated by a regex
    personnummer = models.CharField(max_length=11, unique=True, validators=[personnummer_regex])
    # Image field for profile picture, with default image, size and dimension validators
    image = models.ImageField(
        upload_to='images/', 
        default='../default_profile_l2i70s', 
        validators=[validate_image_file_size, validate_image_dimensions]
    )
    # Auto-generated fields for creation and update timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    @property
    def full_name(self):
        # A convenience property to get the full name of the user
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        # The string representation of the object, which is helpful for admin and debugging purposes
        return f"{self.first_name} {self.last_name}"
