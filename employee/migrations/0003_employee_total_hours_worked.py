# Generated by Django 4.2.7 on 2024-05-01 19:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0002_remove_employee_total_hours_worked_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='total_hours_worked',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
