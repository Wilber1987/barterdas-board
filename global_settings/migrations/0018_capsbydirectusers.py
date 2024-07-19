# Generated by Django 4.1.5 on 2023-07-24 03:04

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        (
            "global_settings",
            "0017_tradingplans_kitplanunilevelpercentage_kit_plan_and_more",
        ),
    ]

    operations = [
        migrations.CreateModel(
            name="CapsByDirectUsers",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "count_of_direct_users",
                    models.PositiveSmallIntegerField(
                        verbose_name="Cantidad de usuarios directos requeridos"
                    ),
                ),
                (
                    "level_to_win",
                    models.PositiveSmallIntegerField(
                        verbose_name="Nivel que podrá generar ganancias"
                    ),
                ),
                (
                    "enabled",
                    models.BooleanField(default=True, verbose_name="Habilitado"),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="Creado en"),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="Modificado en"),
                ),
            ],
            options={
                "verbose_name": "Cantidad de usuarios directos para ganar",
                "verbose_name_plural": "Cantidad de usuarios directos para ganar",
            },
        ),
    ]