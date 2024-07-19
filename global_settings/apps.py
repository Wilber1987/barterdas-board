from django.apps import AppConfig


class GlobalSettingsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'global_settings'
    verbose_name = 'Configuracion global'
    
    def ready(self):
        from global_settings.signals import businesswallet_signals