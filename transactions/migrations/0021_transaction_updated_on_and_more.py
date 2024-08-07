# Generated by Django 4.1.5 on 2023-03-31 22:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0020_alter_dailypercentagerevenue_percentage_amount_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='updated_on',
            field=models.DateTimeField(auto_now=True, verbose_name='Actualizado en'),
        ),
        migrations.AddField(
            model_name='transaction',
            name='wallet_deposit_date',
            field=models.DateTimeField(null=True, verbose_name='Fecha de deposito en wallet'),
        ),
    ]
