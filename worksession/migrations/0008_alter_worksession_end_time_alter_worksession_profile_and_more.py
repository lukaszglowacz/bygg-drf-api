# Generated by Django 4.2.7 on 2024-04-11 23:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0003_alter_profile_user'),
        ('workplace', '0001_initial'),
        ('worksession', '0007_remove_worksession_user_worksession_profile_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='worksession',
            name='end_time',
            field=models.DateTimeField(verbose_name='Czas zakończenia'),
        ),
        migrations.AlterField(
            model_name='worksession',
            name='profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='profiles.profile', verbose_name='Profil użytkownika'),
        ),
        migrations.AlterField(
            model_name='worksession',
            name='start_time',
            field=models.DateTimeField(verbose_name='Czas rozpoczęcia'),
        ),
        migrations.AlterField(
            model_name='worksession',
            name='workplace',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='workplace.workplace', verbose_name='Miejsce pracy'),
        ),
    ]
