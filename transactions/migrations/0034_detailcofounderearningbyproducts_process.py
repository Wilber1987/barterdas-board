# Generated by Django 4.1.5 on 2023-04-29 04:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0033_detailcofounderearningbytrading_process'),
    ]

    operations = [
        migrations.AddField(
            model_name='detailcofounderearningbyproducts',
            name='process',
            field=models.TextField(blank=True, null=True, verbose_name='Procesos de calculo'),
        ),
    ]
