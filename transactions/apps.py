from django.apps import AppConfig
import pycron


class TransactionsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "transactions"
    verbose_name = "Transacciones"
    def ready(self):        
        from transactions.signals import (
            transaction_signals,
            monthly_trading_earnings_signals,
            withdrawal_signals,
            cofounder_earning_by_trading_signals,
            cofounder_earning_by_product_signals,
            reinvestments_signals,
            trading_earnings_signals,            
        )
        from django.core import management
        #management.call_command('CronScheduleCommand')
