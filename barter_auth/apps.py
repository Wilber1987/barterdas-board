from django.apps import AppConfig


class AuthConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'barter_auth'
    verbose_name = 'Usuarios'

    def ready(self):
        from barter_auth.signals import barteruser_signals