# Generated by Django 4.1.5 on 2023-05-10 19:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('global_settings', '0008_userversioning'),
        ('barter_auth', '0023_barteruser_leadership_pool_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='barteruser',
            name='versioning',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='global_settings.userversioning', verbose_name='Creado en'),
        ),
    ]
