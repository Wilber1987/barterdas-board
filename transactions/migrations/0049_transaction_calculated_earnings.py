# Generated by Django 4.1.5 on 2023-05-27 15:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0048_alter_dailypercentagerevenue_percentage_amount'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='calculated_earnings',
            field=models.BooleanField(default=False, verbose_name='Ganancias calculadas'),
        ),
    ]