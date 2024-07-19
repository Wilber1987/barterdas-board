# Generated by Django 4.1.5 on 2023-07-12 12:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('global_settings', '0016_alter_businesswallet_hash'),
    ]

    operations = [
        migrations.CreateModel(
            name='TradingPlans',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=255, verbose_name='Codigo del plan')),
                ('name', models.CharField(max_length=255, verbose_name='Nombre del plan')),
                ('description', models.TextField(verbose_name='Descripcion del plan')),
                ('price', models.DecimalField(decimal_places=4, max_digits=21, verbose_name='Monto del plan')),
                ('cap', models.DecimalField(decimal_places=4, max_digits=21, verbose_name='Tope del plan (%)')),
                ('enabled', models.BooleanField(default=True, verbose_name='Habilitado')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Creado en')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Modificado en')),
            ],
            options={
                'verbose_name': 'Plan de Trading',
                'verbose_name_plural': 'Planes de Trading',
            },
        ),
        migrations.AddField(
            model_name='kitplanunilevelpercentage',
            name='kit_plan',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='unilevel_percentages', to='global_settings.kitplan', verbose_name='Kit Plan'),
        ),
        migrations.AddField(
            model_name='tradingunilevelpercentage',
            name='trading_plan',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='trading_unilevel_percentages', to='global_settings.tradingplans', verbose_name='Plan de trading'),
        ),
    ]