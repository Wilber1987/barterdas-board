# Generated by Django 4.1.5 on 2023-04-15 22:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('barter_auth', '0020_plansearningsdetail_transaction'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='plansearnings',
            options={'verbose_name': 'Ganancia de Kit Plan por Líder', 'verbose_name_plural': 'Ganancias de Kit Plan por Líder'},
        ),
        migrations.AlterModelOptions(
            name='plansearningsdetail',
            options={'verbose_name': 'Detalle de las ganancias de Kit Plan por Líder', 'verbose_name_plural': 'Detalles de las ganancias de Kit Plan por Líder'},
        ),
    ]
