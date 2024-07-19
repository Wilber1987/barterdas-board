from django.db import models


# Fields reference
# https://developers.sumsub.com/api-reference/#webhook-types
class KYCVerificationResult(models.Model):
    applicant_id = models.CharField(max_length=255, verbose_name='Aplicante')
    inspection_id = models.CharField(max_length=255, verbose_name='Inspeccion')
    correlation_id = models.CharField(max_length=255, verbose_name='Correlacion')
    external_user_id = models.CharField(max_length=255, verbose_name='Usuario')
    level_name = models.CharField(max_length=255, null=True, blank=True, verbose_name='Nivel')
    type = models.CharField(max_length=255, verbose_name='Tipo')
    review_status = models.CharField(max_length=255, verbose_name='Estado')
    created_at_ms = models.DateTimeField(verbose_name='Creado en')
    json_data = models.JSONField() # To store complete original unprocessed json request data
    
    class Meta:
        verbose_name = 'Verificacion de KYC'
        verbose_name_plural = 'Verificaciones de KYC'
        
    def __str__(self):
        return f'{self.id} - {self.external_user_id} - {self.level_name}'


# Fields reference
# https://developers.sumsub.com/api-reference/#getting-applicant-status-sdk
class KYCReviewResult(models.Model):
    verification_result = models.ForeignKey(KYCVerificationResult, on_delete=models.PROTECT, related_name='review_result', verbose_name='Verificacion de KYC')
    moderation_comment = models.TextField(verbose_name='Comentario interno') # Can be shown to user
    client_comment = models.TextField(verbose_name='Comentario publico') # Internal comment, do not display
    review_answer = models.CharField(max_length=255, verbose_name='Respuesta')
    reject_labels = models.CharField(max_length=255, verbose_name='Rechazado por') # Ideally a many to many field
    review_reject_type = models.CharField(max_length=255, verbose_name='Tipo de rechazo')
    
    class Meta:
        verbose_name = 'Resultado de verificacion de KYC'
        verbose_name_plural = 'Resultados de verificaciones de KYC'
        
    def __str__(self):
        return f'{self.id} - {self.review_answer}'
    
    
# To fill form finished data from frontend
class KYCManualVerificationDetail(models.Model):
    external_user_id = models.ForeignKey('barter_auth.BarterUser', on_delete=models.PROTECT, related_name='kyc_manual_verification_details', verbose_name='Usuario')
    applicant_id = models.CharField(max_length=255, verbose_name='Aplicante')
    level_name = models.CharField(max_length=100, verbose_name='Nivel')
    review_status = models.CharField(max_length=50, verbose_name='Estado')
    review_answer = models.CharField(max_length=50, verbose_name='Respuesta')
    
    class Meta:
        verbose_name = 'Registro de frontend de KYC'
        verbose_name_plural = 'Registros de frontend de KYC'
        
    def __str__(self):
        return f'{self.id} - {self.external_user_id} - {self.level_name} - {self.review_answer}'