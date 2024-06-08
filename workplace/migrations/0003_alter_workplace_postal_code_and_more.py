# Generated by Django 4.2.7 on 2024-06-08 11:32

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workplace', '0002_alter_workplace_postal_code_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workplace',
            name='postal_code',
            field=models.CharField(max_length=7, validators=[django.core.validators.RegexValidator(message="Postal code format: 'XXX XX'", regex='^\\d{3}\\s\\d{2}$')]),
        ),
        migrations.AlterField(
            model_name='workplace',
            name='street_number',
            field=models.CharField(max_length=10, validators=[django.core.validators.RegexValidator(message='Street number must be numeric', regex='^\\d+$')]),
        ),
    ]
