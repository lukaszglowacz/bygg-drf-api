# Generated by Django 4.2.7 on 2024-04-12 08:48

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0003_alter_profile_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='personnummer',
            field=models.CharField(max_length=11, unique=True, validators=[django.core.validators.RegexValidator(message='RRMMDD-XXXX', regex='^\\d{6}-\\d{4}$')]),
        ),
    ]
