# Generated by Django 4.1.5 on 2023-04-28 20:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0031_dailypercentagerevenue_created_at_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userdailytradingrevenue',
            old_name='trading_transaction',
            new_name='transaction',
        ),
    ]