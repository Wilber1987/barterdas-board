# Generated by Django 4.1.5 on 2023-04-14 20:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales_funnel', '0002_alter_newslettersubscription_subscriptor_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='salesfunnelowner',
            name='custom_video_url',
            field=models.URLField(blank=True, verbose_name='Video de Youtube'),
        ),
        migrations.AlterField(
            model_name='salesfunnelowner',
            name='facebook_account_url',
            field=models.URLField(blank=True, verbose_name='Enlace de Facebook'),
        ),
        migrations.AlterField(
            model_name='salesfunnelowner',
            name='profile_image',
            field=models.ImageField(blank=True, upload_to='', verbose_name='Imagen de perfil'),
        ),
        migrations.AlterField(
            model_name='salesfunnelowner',
            name='twitter_account_url',
            field=models.URLField(blank=True, verbose_name='Enlace de Twitter'),
        ),
        migrations.AlterField(
            model_name='salesfunnelowner',
            name='whatsapp_phone_number',
            field=models.CharField(blank=True, max_length=15, verbose_name='Numero de Whatsapp'),
        ),
    ]
