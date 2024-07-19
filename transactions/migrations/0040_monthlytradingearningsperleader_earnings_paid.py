# Generated by Django 4.1.5 on 2023-05-03 04:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0039_alter_reinvestments_type_re_investment'),
    ]

    operations = [
        migrations.AddField(
            model_name='monthlytradingearningsperleader',
            name='earnings_paid',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Ganancias pagadas'),
            preserve_default=False,
        ),
    ]