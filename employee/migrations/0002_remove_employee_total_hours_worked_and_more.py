# Generated by Django 4.2.7 on 2024-05-01 18:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0004_alter_profile_personnummer'),
        ('employee', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employee',
            name='total_hours_worked',
        ),
        migrations.AlterField(
            model_name='employee',
            name='profile',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='employee', to='profiles.profile'),
        ),
    ]