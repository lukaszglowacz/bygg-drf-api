# Generated by Django 3.2.20 on 2024-03-24 11:50

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Workplace',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('street', models.CharField(max_length=255)),
                ('street_number', models.CharField(max_length=10, validators=[django.core.validators.RegexValidator(message='Numer ulicy musi być liczbą.', regex='^\\d+$')])),
                ('postal_code', models.CharField(max_length=7, validators=[django.core.validators.RegexValidator(message="Kod pocztowy musi być w formacie 'XXX XX'.", regex='^\\d{3}\\s\\d{2}$')])),
                ('city', models.CharField(max_length=255)),
            ],
        ),
    ]
