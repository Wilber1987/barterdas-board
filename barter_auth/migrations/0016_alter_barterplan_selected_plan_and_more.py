# Generated by Django 4.1.5 on 2023-03-16 12:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('barter_auth', '0015_alter_barterplan_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='barterplan',
            name='selected_plan',
            field=models.PositiveSmallIntegerField(choices=[(20, '$20'), (50, '$50'), (100, '$100'), (200, '$200'), (400, '$400'), (800, '$800'), (1000, '$1000')], default=20, verbose_name='Plan seleccionado'),
        ),
        migrations.AlterField(
            model_name='barterplan',
            name='transaction_hash',
            field=models.CharField(max_length=250, verbose_name='Hash de transacción'),
        ),
        migrations.AlterField(
            model_name='barterplan',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='plans', to=settings.AUTH_USER_MODEL, verbose_name='Usuario'),
        ),
        migrations.AlterField(
            model_name='barterplancredentials',
            name='description',
            field=models.CharField(max_length=250, verbose_name='Plataforma'),
        ),
        migrations.AlterField(
            model_name='barterplancredentials',
            name='end_date',
            field=models.DateField(verbose_name='Fecha de finalización'),
        ),
        migrations.AlterField(
            model_name='barterplancredentials',
            name='password',
            field=models.CharField(max_length=250, verbose_name='Clave'),
        ),
        migrations.AlterField(
            model_name='barterplancredentials',
            name='plan',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='credentials', to='barter_auth.barterplan', verbose_name='Plan'),
        ),
        migrations.AlterField(
            model_name='barterplancredentials',
            name='start_date',
            field=models.DateField(verbose_name='Fecha de inicio'),
        ),
        migrations.AlterField(
            model_name='barterplancredentials',
            name='username',
            field=models.CharField(max_length=250, verbose_name='Usuario'),
        ),
        migrations.AlterField(
            model_name='bartertradingplan',
            name='trading_amount',
            field=models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Inversión'),
        ),
        migrations.AlterField(
            model_name='bartertradingplan',
            name='transaction_hash',
            field=models.CharField(max_length=250, verbose_name='Hash de transacción'),
        ),
        migrations.AlterField(
            model_name='bartertradingplan',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='Usuario'),
        ),
    ]
