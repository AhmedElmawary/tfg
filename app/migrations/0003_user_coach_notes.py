# Generated by Django 2.2.6 on 2020-02-09 15:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coachapp', '0001_initial'),
        ('app', '0002_auto_20200209_1203'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='coach_notes',
            field=models.ManyToManyField(blank=True, null=True, to='coachapp.CoachNote'),
        ),
    ]
