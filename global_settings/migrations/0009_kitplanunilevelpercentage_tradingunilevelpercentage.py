# Generated by Django 4.1.5 on 2023-05-23 03:45

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('global_settings', '0008_userversioning'),
    ]

    operations = [
        migrations.CreateModel(
            name='KitPlanUnilevelPercentage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, unique=True, verbose_name='Nombre')),
                ('description', models.CharField(blank=True, max_length=100, verbose_name='Descripcion')),
                ('level', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(10)], verbose_name='Nivel')),
                ('earnings_percentage', models.DecimalField(decimal_places=3, max_digits=6, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(1)], verbose_name='Porcentaje de ganancia de nivel')),
                ('enabled', models.BooleanField(verbose_name='Habilitado')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Creado en')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Modificado en')),
            ],
            options={
                'verbose_name': 'Porcentaje de ganancia por nivel de Kit Plan',
                'verbose_name_plural': 'Porcentajes de ganancia por nivel de Kit Plan',
            },
        ),
        migrations.CreateModel(
            name='TradingUnilevelPercentage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, unique=True, verbose_name='Nombre')),
                ('description', models.CharField(blank=True, max_length=100, verbose_name='Descripcion')),
                ('level', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(10)], verbose_name='Nivel')),
                ('earnings_percentage', models.DecimalField(decimal_places=3, max_digits=6, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(1)], verbose_name='Porcentaje de ganancia de nivel')),
                ('enabled', models.BooleanField(verbose_name='Habilitado')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Creado en')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Modificado en')),
            ],
            options={
                'verbose_name': 'Porcentaje de ganancia por nivel de Trading',
                'verbose_name_plural': 'Porcentajes de ganancia por nivel de Trading',
            },
        ),
    ]