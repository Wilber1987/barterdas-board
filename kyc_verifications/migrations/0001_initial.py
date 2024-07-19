# Generated by Django 4.1.5 on 2023-04-17 17:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='KYCVerificationResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('applicant_id', models.CharField(max_length=255)),
                ('inspection_id', models.CharField(max_length=255)),
                ('correlation_id', models.CharField(max_length=255)),
                ('level_name', models.CharField(blank=True, max_length=255, null=True)),
                ('type', models.CharField(max_length=255)),
                ('review_status', models.CharField(max_length=255)),
                ('created_at_ms', models.DateTimeField()),
                ('json_data', models.JSONField()),
                ('external_user_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='kyc_verifications', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='KYCReviewResults',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('moderation_comment', models.TextField()),
                ('client_comment', models.TextField()),
                ('review_answer', models.CharField(max_length=255)),
                ('reject_labels', models.CharField(max_length=255)),
                ('review_reject_type', models.CharField(max_length=255)),
                ('verification_result', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='review_result', to='kyc_verifications.kycverificationresult')),
            ],
        ),
    ]
