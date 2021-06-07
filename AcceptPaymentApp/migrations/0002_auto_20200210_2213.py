# Generated by Django 2.2.6 on 2020-02-10 22:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('AcceptPaymentApp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='package_payment_user', to=settings.AUTH_USER_MODEL),
        ),
    ]
