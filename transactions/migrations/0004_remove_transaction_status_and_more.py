# Generated by Django 4.1.5 on 2023-02-08 07:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0003_transaction_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transaction',
            name='status',
        ),
        migrations.RemoveField(
            model_name='transaction',
            name='transaction_hash',
        ),
        migrations.AddField(
            model_name='transaction',
            name='exchanges',
            field=models.CharField(default=None, max_length=150),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='transaction',
            name='transaction_type',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.PROTECT, to='transactions.transactiontype'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='transaction',
            name='amount',
            field=models.FloatField(default=0.0),
            preserve_default=False,
        ),
    ]
