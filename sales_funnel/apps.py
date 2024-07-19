from django.apps import AppConfig


class SalesFunnelConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'sales_funnel'
    verbose_name = 'Embudo de ventas'

    def ready(self):
        # Import and register your signal receivers here
        import sales_funnel.signals