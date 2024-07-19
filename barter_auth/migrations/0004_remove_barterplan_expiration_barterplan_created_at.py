# Generated by Django 4.1.5 on 2023-02-09 07:02

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('barter_auth', '0003_alter_barterplan_expiration_bartertradingplan'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='barterplan',
            name='expiration',
        ),
        migrations.AddField(
            model_name='barterplan',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]