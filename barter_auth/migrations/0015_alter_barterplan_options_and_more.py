# Generated by Django 4.1.5 on 2023-03-08 04:04

import barter_auth.utils
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('barter_auth', '0014_barterplancredentials_end_date_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='barterplan',
            options={'verbose_name': 'Compra de Kit plan', 'verbose_name_plural': 'Compras de Kit plans'},
        ),
        migrations.AlterModelOptions(
            name='barterplancredentials',
            options={'verbose_name': 'Credencial de Kit Plan', 'verbose_name_plural': 'Credenciales de Kit Plans'},
        ),
        migrations.AlterModelOptions(
            name='bartertradingplan',
            options={'verbose_name': 'Inversion de trading', 'verbose_name_plural': 'Inversiones de trading'},
        ),
        migrations.AlterModelOptions(
            name='barterusernode',
            options={'verbose_name': 'Referido', 'verbose_name_plural': 'Referidos'},
        ),
        migrations.AlterModelOptions(
            name='barterusersecurityprofile',
            options={'verbose_name': 'Perfil de seguridad', 'verbose_name_plural': 'Perfiles de seguridad'},
        ),
        migrations.AlterField(
            model_name='barteruser',
            name='address',
            field=models.CharField(blank=True, max_length=250, null=True, verbose_name='Direccion'),
        ),
        migrations.AlterField(
            model_name='barteruser',
            name='city',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Ciudad'),
        ),
        migrations.AlterField(
            model_name='barteruser',
            name='country',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Pais'),
        ),
        migrations.AlterField(
            model_name='barteruser',
            name='is_co_founder',
            field=models.BooleanField(default=False, verbose_name='Es cofundador'),
        ),
        migrations.AlterField(
            model_name='barteruser',
            name='phone_number',
            field=models.CharField(blank=True, max_length=25, null=True, verbose_name='Telefono'),
        ),
        migrations.AlterField(
            model_name='barteruser',
            name='profile_image',
            field=models.URLField(default=barter_auth.utils.generate_default_image, verbose_name='Imagen de perfil'),
        ),
        migrations.AlterField(
            model_name='barteruser',
            name='referral_code',
            field=models.CharField(blank=True, default=barter_auth.utils.generate_referral_code, max_length=250, null=True, unique=True, verbose_name='Codigo de referido'),
        ),
        migrations.AlterField(
            model_name='barteruser',
            name='referrals',
            field=models.ManyToManyField(through='barter_auth.Referral', to=settings.AUTH_USER_MODEL, verbose_name='Referidos'),
        ),
        migrations.AlterField(
            model_name='barteruser',
            name='verified',
            field=models.BooleanField(default=False, verbose_name='Verificado'),
        ),
        migrations.AlterField(
            model_name='barteruser',
            name='zip_code',
            field=models.CharField(blank=True, max_length=10, null=True, verbose_name='Codigo Postal'),
        ),
        migrations.AlterField(
            model_name='barterusersecurityprofile',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='security_profiles', to=settings.AUTH_USER_MODEL),
        ),
    ]
