from django.db import models
from django.core.validators import RegexValidator

# Validator for ensuring the street number is numeric
street_number_regex = RegexValidator(regex=r'^\d+$', message="Street number must be numeric")

# Validator for the postal code to match specific format (e.g., '123 45')
postal_code_regex = RegexValidator(regex=r'^\d{3}\s\d{2}$', message="Postal code format: 'XXX XX'")

class Workplace(models.Model):
    # Field to store the street name with a max length constraint
    street = models.CharField(max_length=255)
    
    # Field to store the street number, validated to ensure it contains only digits
    street_number = models.CharField(max_length=10, validators=[street_number_regex])
    
    # Field to store the postal code, validated to match the Swedish postal code format
    postal_code = models.CharField(max_length=7, validators=[postal_code_regex])
    
    # Field to store the city name with a max length constraint
    city = models.CharField(max_length=255)
    
    def __str__(self):
        # Returns a string representation of the workplace, formatting address components neatly
        return f"{self.street} {self.street_number}, {self.postal_code} {self.city}"
