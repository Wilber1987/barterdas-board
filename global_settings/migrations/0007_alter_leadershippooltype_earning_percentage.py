# Generated by Django 4.1.5 on 2023-05-02 20:42

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('global_settings', '0006_leadershippooltype'),
    ]

    operations = [
        migrations.AlterField(
            model_name='leadershippooltype',
            name='earning_percentage',
            field=models.DecimalField(decimal_places=3, max_digits=6, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(1.0)], verbose_name='Porcentaje de ganancia'),
        ),
    ]
