# Generated by Django 4.1.5 on 2023-04-05 04:04

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='WithdrawalType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=100, unique=True, verbose_name='Descripcion')),
                ('value', models.PositiveSmallIntegerField(unique=True, verbose_name='Valor')),
                ('enabled', models.BooleanField(verbose_name='Habilitado')),
            ],
        ),
    ]
