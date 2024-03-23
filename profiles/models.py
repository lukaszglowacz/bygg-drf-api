from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import RegexValidator

personnummer_regex = RegexValidator(regex=r'^\d{6}-\d{4}$', message='XXXXXX-XXXX')

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    personnummer = models.CharField(max_length=11, unique=True, validators=[personnummer_regex])
    image = models.ImageField(upload_to='images/', default='../default_profile_l2i70s')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username
    
# Tworzenie profilu uzytkownika po utworzeniu konta
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

# Aktualizacja profilu po zapisaniu uzytkownika
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()