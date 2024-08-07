# Generated by Django 4.1.5 on 2023-04-28 14:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('transactions', '0030_alter_withdrawal_amount_after_fee_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='CoFounderEarningByProducts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('earning_percentage', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Porcentaje de ganancias')),
                ('product', models.IntegerField(choices=[(0, 'Dashboard'), (1, 'Wallet'), (2, 'Streaming'), (3, 'Marketing')], verbose_name='Producto')),
                ('month', models.IntegerField(choices=[(1, 'January'), (2, 'February'), (3, 'March'), (4, 'April'), (5, 'May'), (6, 'June'), (7, 'July'), (8, 'August'), (9, 'September'), (10, 'October'), (11, 'November'), (12, 'December')], default=4, verbose_name='Mes')),
                ('trimester', models.IntegerField(verbose_name='Trimestre, campo calculado automáticamente')),
                ('year', models.IntegerField(default=2023, verbose_name='Año')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Creado en')),
            ],
            options={
                'verbose_name': 'Ganancia de cofundador por producto',
                'verbose_name_plural': 'Ganancias de cofundador por producto',
            },
        ),
        migrations.CreateModel(
            name='CoFounderEarningByTrading',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('earning_percentage', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Porcentaje de ganancias')),
                ('month', models.IntegerField(choices=[(1, 'January'), (2, 'February'), (3, 'March'), (4, 'April'), (5, 'May'), (6, 'June'), (7, 'July'), (8, 'August'), (9, 'September'), (10, 'October'), (11, 'November'), (12, 'December')], default=4, verbose_name='Mes')),
                ('trimester', models.IntegerField(verbose_name='Trimestre, campo calculado automáticamente')),
                ('year', models.IntegerField(default=2023, verbose_name='Año')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Creado en')),
            ],
            options={
                'verbose_name': 'Ganancia de cofundador por trading',
                'verbose_name_plural': 'Ganancias de cofundador por trading',
            },
        ),
        migrations.CreateModel(
            name='DetailCoFounderEarningByTrading',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('earnings', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Ganancias')),
                ('earnings_paid', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Ganancias pagadas')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Creado en')),
                ('co_founder_earning_by_trading', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='details', to='transactions.cofounderearningbytrading')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='co_founder_earning_by_trading', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Detalle de ganancia de cofundador por trading',
                'verbose_name_plural': 'Detalles de ganancia de cofundador por trading',
            },
        ),
        migrations.CreateModel(
            name='DetailCoFounderEarningByProducts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('earnings', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Ganancias')),
                ('earnings_paid', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Ganancias pagadas')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Creado en')),
                ('co_founder_earning_by_products', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='details', to='transactions.cofounderearningbyproducts')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='co_founder_earning_by_products', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Detalle de ganancia de cofundador por producto',
                'verbose_name_plural': 'Detalles de ganancia de cofundador por producto',
            },
        ),
    ]
