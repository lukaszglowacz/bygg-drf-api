# Importing necessary modules and functions from Django
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _

# CustomUserManager: Custom manager for user model handling user creation and superuser creation.
class CustomUserManager(BaseUserManager):
    # Method to create a regular user with the provided email and password.
    def create_user(self, email, password=None, **extra_fields):
        # Ensuring an email is provided, if not, raise a ValueError
        if not email:
            raise ValueError(_('The Email field must be set'))
        # Normalizing the provided email.
        email = self.normalize_email(email)
        # Creating a user instance with the normalized email and extra fields.
        user = self.model(email=email, **extra_fields)
        # Setting user's password which also hashes it.
        user.set_password(password)
        # Saving the user to the database.
        user.save(using=self._db)
        return user

    # Method to create a superuser with all permissions enabled.
    def create_superuser(self, email, password=None, **extra_fields):
        # Setting flags for is_staff and is_superuser to True for superuser.
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        # Creating and returning a superuser using the create_user method.
        return self.create_user(email, password, **extra_fields)

# CustomUser: Custom user model inheriting from AbstractUser.
class CustomUser(AbstractUser):
    # Removing username field and using email as the main identifier.
    username = None
    # Adding an email field that is unique and required.
    email = models.EmailField(_('email address'), unique=True, error_messages={
        'unique': _("This email address is already in use. Please use a different address."),
    })
    
    # Adding an 'is_employer' field to differentiate types of users (optional).
    is_employer = models.BooleanField(default=False)

    # Setting the email field as the unique identifier for authentication.
    USERNAME_FIELD = 'email'
    # Making email the only required field.
    REQUIRED_FIELDS = []

    # Assigning CustomUserManager to handle objects of this model.
    objects = CustomUserManager()

    # String representation of the model, returning the user's email.
    def __str__(self):
        return self.email
