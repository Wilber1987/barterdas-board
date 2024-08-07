# Generated by Django 4.1.5 on 2023-04-15 20:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sales_funnel', '0005_alter_newslettersubscription_enabled_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='FunnelStep',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('step_number', models.PositiveSmallIntegerField(verbose_name='No. de paso')),
                ('title', models.CharField(max_length=100, verbose_name='Titulo')),
                ('youtube_video_url', models.URLField(verbose_name='Enlace de video en Youtube')),
                ('enabled', models.BooleanField(default=True, verbose_name='Habilitado')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Creado en')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Modificado en')),
                ('next_step', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='previous_step', to='sales_funnel.funnelstep', verbose_name='Siguiente paso')),
            ],
            options={
                'verbose_name': 'Paso de embudo de venta',
                'verbose_name_plural': 'Pasos de embudo de ventas',
            },
        ),
    ]
