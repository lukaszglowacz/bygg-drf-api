from django.test import TestCase
from .models import Workplace
from django.core.exceptions import ValidationError

class WorkplaceModelTests(TestCase):

    def setUp(self):
        self.workplace = Workplace.objects.create(
            street='Main',
            street_number='123',
            postal_code='123 45',
            city='Sample City'
        )

    def test_workplace_creation(self):
        self.assertEqual(self.workplace.street, 'Main')
        self.assertEqual(self.workplace.street_number, '123')
        self.assertEqual(self.workplace.postal_code, '123 45')
        self.assertEqual(self.workplace.city, 'Sample City')
        self.assertEqual(str(self.workplace), 'Main 123, 123 45 Sample City')

    def test_invalid_street_number(self):
        with self.assertRaises(ValidationError):
            workplace = Workplace(
                street='Main',
                street_number='ABC',  # Invalid street number
                postal_code='123 45',
                city='Sample City'
            )
            workplace.full_clean()

    def test_invalid_postal_code(self):
        with self.assertRaises(ValidationError):
            workplace = Workplace(
                street='Main',
                street_number='123',
                postal_code='12345',  # Invalid postal code format
                city='Sample City'
            )
            workplace.full_clean()
