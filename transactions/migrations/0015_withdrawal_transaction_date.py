# Generated by Django 4.1.5 on 2023-03-08 04:55

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0013_withdrawal'),
    ]

    operations = [
        migrations.AddField(
            model_name='withdrawal',
            name='transaction_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
