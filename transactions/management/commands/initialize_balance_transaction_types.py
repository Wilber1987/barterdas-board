from django.core.management import BaseCommand
from transactions.models import BalanceTransactionType


class Command(BaseCommand):
    help = "Command to generate initial instances of BalanceTransactionType model"

    def handle(self, *args, **kwargs):
        dataset = [  # Initial values by Axel and me
            {
                "name": "Deposito a balance general",
                "description": "",
                "app_lookup": "",
                "model_lookup": "",
                "balance_lookup_field": "general_balance",
                "is_income": True,
                "unique_code": "DGB",  # Deposit General Balance
            },
            {
                "name": "Compra de plan de trading",
                "description": "",
                "app_lookup": "transactions",
                "model_lookup": "Transaction",
                "balance_lookup_field": "trading_balance",
                "is_income": True,
                "unique_code": "PTT",  # Purchase transaction trading
            },
            {
                "name": "Compra de kit plan",
                "description": "",
                "app_lookup": "transactions",
                "model_lookup": "Transaction",
                "balance_lookup_field": "kitplan_balance",
                "is_income": True,
                "unique_code": "PTK",  # Purchase transaction Kitplan
            },
            {
                "name": "Compra de plan de cofundador",
                "description": "",
                "app_lookup": "transactions",
                "model_lookup": "Transaction",
                "balance_lookup_field": "cofounder_balance",
                "is_income": True,
                "unique_code": "PTC",  # Purchase transaction Cofounder
            },
            {
                "name": "Ganancias de red de kit plan",
                "description": "",
                "app_lookup": "transactions",
                "model_lookup": "KitPlanNetWorkEarnings",
                "balance_lookup_field": "kitplan_network_earnings",
                "is_income": True,
                "unique_code": "EKN",  # Deposit transaction Kitplan
            },
            # * Waiting until monthly trading earnings is finished
            # {
            #     "name": "Ganancias personales mensuales de trading",
            #     "description": "",
            #     "app_lookup": "transactions",
            #     "model_lookup": "Transaction",
            #     "balance_lookup_field": "kitplan_balance",
            #     "is_income": True,
            #     "unique_code": "ETP"
            # },
            {
                "name": "Retiro de ganancias personales de trading",
                "description": "",
                "app_lookup": "transactions",
                "model_lookup": "Withdrawal",
                "balance_lookup_field": "trading_earnings",
                "is_income": False,
                "unique_code": "WTPE",  # Withdrawal Trading Personal Earnings
            },
            {
                "name": "Retiro de ganancias de red de trading",
                "description": "",
                "app_lookup": "transactions",
                "model_lookup": "Withdrawal",
                "balance_lookup_field": "trading_network_earnings",
                "is_income": False,
                "unique_code": "WTNE",  # Withdrawal Trading Network Earnings
            },
            {
                "name": "Retiro de ganancias de red de kit plan",
                "description": "",
                "app_lookup": "transactions",
                "model_lookup": "Withdrawal",
                "balance_lookup_field": "kitplan_network_earnings",
                "is_income": False,
                "unique_code": "WKNE",  # Withdrawal Kitplan Network Earnings
            },
            {
                "name": "Retiro de ganancias de cofundador",
                "description": "",
                "app_lookup": "transactions",
                "model_lookup": "Withdrawal",
                "balance_lookup_field": "cofounder_earnings",
                "is_income": False,
                "unique_code": "WCPE",  # Withdrawal Cofounder Personal Earnings
            },
            {
                "name": "Ganancias mensuales de producto de cofundador",
                "description": "",
                "app_lookup": "transactions",
                "model_lookup": "DetailCoFouderEarningByProducts",
                "balance_lookup_field": "cofounder_earnings",
                "is_income": True,
                "unique_code": "CMPE",  # Cofounder Monthly Product Earnings
            },
            {
                "name": "Ganancias mensuales de trading de cofundador",
                "description": "",
                "app_lookup": "transactions",
                "model_lookup": "DetailCoFouderEarningByTrading",
                "balance_lookup_field": "cofounder_earnings",
                "is_income": True,
                "unique_code": "CMTE",  # Cofounder Monthly Trading Earnings
            },
            {
                "name": "Reinversión de ganancias personales de trading",
                "description": "",
                "app_lookup": "transactions",
                "model_lookup": "ReInvestments",
                "balance_lookup_field": "trading_earnings",
                "is_income": False,
                "unique_code": "RTPE",  # Reinvest Trading Personal Earnings
            },
            {
                "name": "Reinversión de ganancias de red de trading",
                "description": "",
                "app_lookup": "transactions",
                "model_lookup": "ReInvestments",
                "balance_lookup_field": "trading_network_earnings",
                "is_income": False,
                "unique_code": "RTNE",  # Reinvest Trading Network Earnings
            },
            {
                "name": "Reinversión de ganancias de cofundador",
                "description": "",
                "app_lookup": "transactions",
                "model_lookup": "ReInvestments",
                "balance_lookup_field": "cofounder_earnings",
                "is_income": False,
                "unique_code": "RCPE",  # Reinvest Cofounder Personal Earnings
            },
        ]

        for data in dataset:
            instance, created = BalanceTransactionType.objects.get_or_create(**data)

            if created:
                print(f"Created {instance.name}")
            else:
                print(f"Fetched {instance.name}")

        print("All initial balance transaction type instances processed")