# Generated by Django 2.2.6 on 2020-02-16 19:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_sessionattendancerequest_joined'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sessionattendancerequest',
            name='joined',
            field=models.BooleanField(default=False),
        ),
    ]
