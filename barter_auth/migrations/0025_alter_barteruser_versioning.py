# Generated by Django 4.1.5 on 2023-05-10 19:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('global_settings', '0008_userversioning'),
        ('barter_auth', '0024_barteruser_versioning'),
    ]

    operations = [
        migrations.AlterField(
            model_name='barteruser',
            name='versioning',
            field=models.ForeignKey(default=1, null=True, on_delete=django.db.models.deletion.PROTECT, to='global_settings.userversioning', verbose_name='Creado en'),
        ),
    ]