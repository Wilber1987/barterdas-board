# Generated by Django 4.1.5 on 2023-02-27 09:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('barter_auth', '0011_barterplancredentials'),
    ]

    operations = [
        migrations.AddField(
            model_name='barterplancredentials',
            name='description',
            field=models.CharField(default='', max_length=250),
            preserve_default=False,
        ),
    ]
