from django.db import models
from django.core.validators import RegexValidator

street_regex = RegexValidator(regex=r'^\d+$', message="Numer ulicy musi być liczbą.")
postal_regex = RegexValidator(regex=r'^\d{3}\s\d{2}$', message="Kod pocztowy musi być w formacie 'XXX XX'.")

class Workplace(models.Model):
    street = models.CharField(max_length=255)
    street_number = models.CharField(max_length=10, validators=[street_regex])
    postal_code = models.CharField(max_length=7, validators=[postal_regex])
    city = models.CharField(max_length=255)

    def save(self, *args, **kwargs):
        self.street = self.street.title()
        self.city = self.street.title()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.street} {self.street_number}, {self.postal_code} {self.city}"