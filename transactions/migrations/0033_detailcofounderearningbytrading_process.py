# Generated by Django 4.1.5 on 2023-04-29 03:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0032_alter_cofounderearningbyproducts_trimester_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='detailcofounderearningbytrading',
            name='process',
            field=models.TextField(blank=True, null=True, verbose_name='Procesos de calculo'),
        ),
    ]
