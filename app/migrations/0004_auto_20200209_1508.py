# Generated by Django 2.2.6 on 2020-02-09 15:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_user_coach_notes'),
    ]

    operations = [
        migrations.AddField(
            model_name='package',
            name='is_bronze',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='package',
            name='is_silver',
            field=models.BooleanField(default=False),
        ),
    ]