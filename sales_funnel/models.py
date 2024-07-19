from django.db import models
from barter_auth.models import BarterUser
from .custom_storage import MediaStorage, FunnelStepThumbnailImageStorage
from django.core.validators import FileExtensionValidator
import os

def get_image_filename(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{instance.username}.{ext}"
    return filename

class SalesFunnelOwner(models.Model):
    user = models.ForeignKey(BarterUser, on_delete=models.PROTECT, related_name='sales_funnel', verbose_name='Usuario')

    # used as the sales funnel endpoint, can only be modified once
    username = models.CharField(max_length=30, unique=True, verbose_name='Nombre en enlace de embudo')
    display_name = models.CharField(max_length=120, verbose_name='Nombre a mostrar')

    # fields to be displayed on the sales funnel
    email = models.EmailField(max_length=254, verbose_name='Email')
    whatsapp_phone_number = models.CharField(max_length=15, blank=True, verbose_name='Numero de Whatsapp')
    facebook_account_url = models.URLField(max_length=200, blank=True, verbose_name='Enlace de Facebook')
    twitter_account_url = models.URLField(max_length=200, blank=True, verbose_name='Enlace de Twitter')
    custom_video_url = models.URLField(max_length=200, blank=True, verbose_name='Video de Youtube')

    profile_image = models.ImageField(blank=True, upload_to=get_image_filename, storage=MediaStorage(), validators=[FileExtensionValidator(allowed_extensions=['png', 'jpg', 'jpeg'])], verbose_name='Imagen de perfil', )

    enabled = models.BooleanField(default=True, verbose_name='Habilitado')
    created_at = models.DateTimeField(auto_now_add=True, blank=True, verbose_name='Creado en')
    updated_at = models.DateTimeField(auto_now=True, blank=True, verbose_name='Modificado en')

    class Meta:
        verbose_name = 'Embudo de venta de clientes'
        verbose_name_plural = 'Embudos de venta de clientes'

    def __str__(self):
        return f'{self.user} - {self.user.email}'


class NewsletterSubscription(models.Model):
    subscribed_to = models.ForeignKey(SalesFunnelOwner, on_delete=models.PROTECT, related_name='subscriptions', verbose_name='Suscrito a')
    subscriptor_email = models.EmailField(max_length=254, unique=True, verbose_name='Email de suscriptor')
    sent_emails = models.PositiveSmallIntegerField(default=0, verbose_name='Cant. de emails enviados')

    enabled = models.BooleanField(default=True, verbose_name='Habilitado')
    created_at = models.DateTimeField(auto_now_add=True, blank=True, verbose_name='Creado en')
    updated_at = models.DateTimeField(auto_now=True, blank=True, verbose_name='Modificado en')

    class Meta:
        verbose_name = 'Suscripcion de embudo'
        verbose_name_plural = 'Suscripciones de embudos'

    def __str__(self):
        return f'{self.subscriptor_email}'
    
class FunnelStep(models.Model):
    step_number = models.PositiveSmallIntegerField(verbose_name='No. de paso')
    title = models.CharField(max_length=100, verbose_name='Titulo')
    youtube_video_url = models.URLField(max_length=200, verbose_name='Enlace de video en Youtube')
    next_step = models.ForeignKey('self', on_delete=models.PROTECT, related_name='previous_step', null=True, blank=True, verbose_name='Siguiente paso')
    thumbnail_image = models.ImageField(blank=True, upload_to='', storage=FunnelStepThumbnailImageStorage(), validators=[FileExtensionValidator(allowed_extensions=['png', 'jpg', 'jpeg'])], verbose_name='Imagen de previsualizacion', )

    enabled = models.BooleanField(default=True, verbose_name='Habilitado')
    created_at = models.DateTimeField(auto_now_add=True, blank=True, verbose_name='Creado en')
    updated_at = models.DateTimeField(auto_now=True, blank=True, verbose_name='Modificado en')


    class Meta:
        verbose_name = 'Paso de embudo de venta'
        verbose_name_plural = 'Pasos de embudo de ventas'

    def __str__(self):
        return f'Paso {self.step_number}: {self.title}'