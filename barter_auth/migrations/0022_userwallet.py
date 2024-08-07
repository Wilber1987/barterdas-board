# Generated by Django 4.1.5 on 2023-04-20 15:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('global_settings', '0005_blockchainchoices_exchangechoices_businesswallet'),
        ('barter_auth', '0021_alter_plansearnings_options_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserWallet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hash', models.CharField(max_length=40, unique=True, verbose_name='Hash de la billetera')),
                ('enabled', models.BooleanField(verbose_name='Habilitado')),
                ('blockchain', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='business_user', to='global_settings.blockchainchoices', verbose_name='Blockchain')),
                ('exchange', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='business_user', to='global_settings.exchangechoices', verbose_name='Red/Moneda')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='wallet', to=settings.AUTH_USER_MODEL, verbose_name='Usuario')),
            ],
            options={
                'verbose_name': 'Billetera de Usuario',
                'verbose_name_plural': 'Billeteras de Usuario',
            },
        ),
    ]
