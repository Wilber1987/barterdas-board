# Generated by Django 4.1.5 on 2023-04-28 22:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0032_rename_trading_transaction_userdailytradingrevenue_transaction'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userdailytradingrevenue',
            old_name='percentage_revenue',
            new_name='daily_percentage_revenue',
        ),
    ]