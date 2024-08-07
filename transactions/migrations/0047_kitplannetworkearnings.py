# Generated by Django 4.1.5 on 2023-05-23 03:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('barter_auth', '0029_plansearningsdetail_level'),
        ('global_settings', '0009_kitplanunilevelpercentage_tradingunilevelpercentage'),
        ('transactions', '0046_balance_balancetransactiontype_balancehistory'),
    ]

    operations = [
        migrations.CreateModel(
            name='KitPlanNetWorkEarnings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('level', models.PositiveIntegerField(verbose_name='Nivel')),
                ('level_earnings_percentage', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Porcentaje de ganancias de nivel')),
                ('current_investment', models.DecimalField(decimal_places=4, max_digits=21, verbose_name='Inversion actual')),
                ('earnings', models.DecimalField(decimal_places=4, max_digits=21, verbose_name='Ganancias')),
                ('calculation_process', models.TextField(blank=True, null=True, verbose_name='Proceso de calculo')),
                ('enabled', models.BooleanField(default=True, verbose_name='Habilitado')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Creado en')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Modificado en')),
                ('kit_plan_unilevel_network', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='kitplan_network_earnings', to='global_settings.kitplanunilevelpercentage', verbose_name='Porcentaje de red de referidos de Kit Plan')),
                ('transaction', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='kitplan_network_earnings', to='transactions.transaction', verbose_name='Transaccion')),
                ('unilevel_network', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='kitplan_network_earnings', to='barter_auth.unilevelnetwork', verbose_name='Red de referidos de Kit Plan')),
            ],
            options={
                'verbose_name': 'Red de referidos de Kit Plan(Ganancias)',
                'verbose_name_plural': 'Red de referidos de Kit Plan(Ganancias)',
            },
        ),
    ]
