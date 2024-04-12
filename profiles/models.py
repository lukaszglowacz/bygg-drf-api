from django.db import models
from django.db.models.signals import post_save
from django.core.validators import RegexValidator
from django.conf import settings
from django.dispatch import receiver
from .validators import validate_image_file_size, validate_image_dimensions

personnummer_regex = RegexValidator(regex=r'^\d{6}-\d{4}$', message='XXXXXX-XXXX')

class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    personnummer = models.CharField(max_length=11, unique=True, validators=[personnummer_regex])
    image = models.ImageField(upload_to='images/', default='../default_profile_l2i70s', validators=[validate_image_file_size, validate_image_dimensions])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.user.email