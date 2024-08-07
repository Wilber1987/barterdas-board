# Generated by Django 4.1.5 on 2023-05-25 17:46

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import global_settings.custom_storage
import global_settings.models


class Migration(migrations.Migration):

    dependencies = [
        ('global_settings', '0010_delete_userversioning'),
    ]

    operations = [
        migrations.CreateModel(
            name='BusinessWalletType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Nombre')),
                ('description', models.TextField(blank=True, verbose_name='Descripción')),
                ('enabled', models.BooleanField(verbose_name='Habilitado')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Creado en')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Modificado en')),
            ],
            options={
                'verbose_name': 'Tipo de Billeteras de empresa',
                'verbose_name_plural': 'Tipos de Billeteras de empresa',
            },
        ),
        migrations.AddField(
            model_name='businesswallet',
            name='qr_code',
            field=models.ImageField(blank=True, storage=global_settings.custom_storage.QRCodeStorage(), upload_to=global_settings.models.get_qr_filename, validators=[django.core.validators.FileExtensionValidator(['jpg', 'png', 'jpeg', 'webp'])], verbose_name='Codigo QR'),
        ),
        migrations.AlterField(
            model_name='businesswallet',
            name='enabled',
            field=models.BooleanField(default=True, verbose_name='Habilitado'),
        ),
        migrations.AddField(
            model_name='businesswallet',
            name='type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='wallets', to='global_settings.businesswallettype', verbose_name='Tipo de billetera'),
        ),
    ]
