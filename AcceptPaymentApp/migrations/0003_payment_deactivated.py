# Generated by Django 2.2.6 on 2020-02-13 13:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AcceptPaymentApp', '0002_auto_20200210_2213'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='deactivated',
            field=models.BooleanField(default=False),
        ),
    ]
