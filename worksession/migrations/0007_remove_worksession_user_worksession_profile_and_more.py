# Generated by Django 4.2.7 on 2024-04-11 21:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0003_alter_profile_user'),
        ('worksession', '0006_alter_worksession_start_time'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='worksession',
            name='user',
        ),
        migrations.AddField(
            model_name='worksession',
            name='profile',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='profiles.profile', verbose_name='Profil użytkownika'),
        ),
        migrations.AlterField(
            model_name='worksession',
            name='end_time',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='worksession',
            name='start_time',
            field=models.DateTimeField(),
        ),
    ]
