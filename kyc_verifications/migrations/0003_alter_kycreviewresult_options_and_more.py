# Generated by Django 4.1.5 on 2023-05-19 16:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('kyc_verifications', '0002_rename_kycreviewresults_kycreviewresult'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='kycreviewresult',
            options={'verbose_name': 'Resultado de verificacion de KYC', 'verbose_name_plural': 'Resultados de verificaciones de KYC'},
        ),
        migrations.AlterModelOptions(
            name='kycverificationresult',
            options={'verbose_name': 'Verificacion de KYC', 'verbose_name_plural': 'Verificaciones de KYC'},
        ),
        migrations.AlterField(
            model_name='kycreviewresult',
            name='client_comment',
            field=models.TextField(verbose_name='Comentario publico'),
        ),
        migrations.AlterField(
            model_name='kycreviewresult',
            name='moderation_comment',
            field=models.TextField(verbose_name='Comentario interno'),
        ),
        migrations.AlterField(
            model_name='kycreviewresult',
            name='reject_labels',
            field=models.CharField(max_length=255, verbose_name='Rechazado por'),
        ),
        migrations.AlterField(
            model_name='kycreviewresult',
            name='review_answer',
            field=models.CharField(max_length=255, verbose_name='Respuesta'),
        ),
        migrations.AlterField(
            model_name='kycreviewresult',
            name='review_reject_type',
            field=models.CharField(max_length=255, verbose_name='Tipo de rechazo'),
        ),
        migrations.AlterField(
            model_name='kycreviewresult',
            name='verification_result',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='review_result', to='kyc_verifications.kycverificationresult', verbose_name='Verificacion de KYC'),
        ),
        migrations.AlterField(
            model_name='kycverificationresult',
            name='applicant_id',
            field=models.CharField(max_length=255, verbose_name='Aplicante'),
        ),
        migrations.AlterField(
            model_name='kycverificationresult',
            name='correlation_id',
            field=models.CharField(max_length=255, verbose_name='Correlacion'),
        ),
        migrations.AlterField(
            model_name='kycverificationresult',
            name='created_at_ms',
            field=models.DateTimeField(verbose_name='Creado en'),
        ),
        migrations.AlterField(
            model_name='kycverificationresult',
            name='external_user_id',
            field=models.CharField(max_length=255, verbose_name='Usuario'),
        ),
        migrations.AlterField(
            model_name='kycverificationresult',
            name='inspection_id',
            field=models.CharField(max_length=255, verbose_name='Inspeccion'),
        ),
        migrations.AlterField(
            model_name='kycverificationresult',
            name='level_name',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Nivel'),
        ),
        migrations.AlterField(
            model_name='kycverificationresult',
            name='review_status',
            field=models.CharField(max_length=255, verbose_name='Estado'),
        ),
        migrations.AlterField(
            model_name='kycverificationresult',
            name='type',
            field=models.CharField(max_length=255, verbose_name='Tipo'),
        ),
        migrations.CreateModel(
            name='KYCManualVerificationDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('applicant_id', models.CharField(max_length=255, verbose_name='Aplicante')),
                ('level_name', models.CharField(max_length=100, verbose_name='Nivel')),
                ('review_status', models.CharField(max_length=50, verbose_name='Estado')),
                ('review_answer', models.CharField(max_length=50, verbose_name='Respuesta')),
                ('external_user_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='kyc_manual_verification_details', to=settings.AUTH_USER_MODEL, verbose_name='Usuario')),
            ],
            options={
                'verbose_name': 'Registro de frontend de KYC',
                'verbose_name_plural': 'Registros de frontend de KYC',
            },
        ),
    ]
