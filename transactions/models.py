# Create your models here.
import calendar

from django.db import models
from django.utils.timezone import now
from django.core.validators import MinValueValidator, MaxValueValidator


class TransactionType(models.Model):
    description = models.CharField(max_length=250)

    def __str__(self):
        return self.description


class Transaction(models.Model):
    TRANSACTION_STATUS = [(0, "IN REVIEW"), (1, "VERIFIED"), (2, "REJECTED")]

    TRANSACTION_TYPE = [
        ("kit-plan", "Kit Plan"),
        ("trading", "Trading"),
        ("co-founder", "Co-founder"),
        ("neutral", "Neutral"),
    ]

    TRANSACTION_WALLET = [
        ("binance", "BINANCE"),
        ("kucoin", "KUCOIN"),
        ("coinbase", "COINBASE"),
        ("bybit", "BYBIT"),
        ("other", "OTHER"),
    ]
    # User who did the transaction
    user = models.ForeignKey(
        'barter_auth.BarterUser',
        on_delete=models.PROTECT,
        related_name="transactions",
        verbose_name="Usuario",
    )
    # Wallet address of the client
    wallet_address = models.CharField(
        max_length=255, verbose_name="Dirección de billetera"
    )
    # Voucher screenshot (this is a URL coming from S3 services)
    voucher_screenshot = models.CharField(
        max_length=255, verbose_name="Captura de voucher"
    )
    # Wallet provider
    wallet_provider = models.CharField(
        max_length=255,
        choices=TRANSACTION_WALLET,
        verbose_name="Proveedor de billetera",
    )
    # This can be taken as Transaction ID
    transaction_hash = models.CharField(
        max_length=250, verbose_name="Hash de transacción"
    )
    # Status of the transaction validated by the tech support staff
    transaction_status = models.IntegerField(
        choices=TRANSACTION_STATUS, default=0, verbose_name="Estado"
    )
    # Description of the transaction
    description = models.CharField(max_length=250, verbose_name="Descripción")
    # Amount paid in this transaction
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Monto")
    # Mark if this transaction is taken as a co-founder investment
    co_founder_invest = models.BooleanField(
        default=False, verbose_name="Inversión de cofundador"
    )
    # Mark transaction type
    transaction_type = models.CharField(
        max_length=250, choices=TRANSACTION_TYPE, verbose_name="Tipo de transacción"
    )
    # Network
    transaction_network = models.CharField(
        max_length=250, default="-", verbose_name="Red/Moneda"
    )
    created_at = models.DateTimeField(default=now, verbose_name="Creado en")
    transaction_date = models.DateTimeField(
        default=now, verbose_name="Fecha de transacción"
    )

    calculated_earnings = models.BooleanField(
        default=False, verbose_name="Ganancias calculadas", blank=True, null=True
    )
    # This date is especified by the finances team
    # It's used in order to calculate revenue
    # 1 day after the value specified
    wallet_deposit_date = models.DateTimeField(
        null=True, verbose_name="Fecha de deposito en wallet"
    )

    # This date is auto_updated in order to have history of modifications
    # Although general updates, instead of transaction_status update
    updated_on = models.DateTimeField(
        auto_now=True, blank=True, editable=False, verbose_name="Actualizado en"
    )

    def __str__(self):
        return f"{self.id} - {self.user.get_full_name()} - {self.amount}"

    class Meta:
        verbose_name = "Transaccion"
        verbose_name_plural = "Transacciones"


class TransactionScreenshot(models.Model):
    transaction = models.ForeignKey(
        Transaction,
        on_delete=models.PROTECT,
        related_name="screenshots",
        verbose_name="Transaccion",
    )
    voucher_screenshot = models.CharField(
        max_length=255, verbose_name="Captura de voucher"
    )
    transaction_date = models.DateField(
        null=True, blank=True, verbose_name="Fecha de transaccion"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Creado en")

    def __str__(self):
        return f"{self.transaction.transaction_hash} - {self.id}"

    class Meta:
        verbose_name = "Captura de transaccion"
        verbose_name_plural = "Capturas de transacciones"


# This model is used to store withdraws
class Withdrawal(models.Model):
    SOURCE_TYPE = [
        ("TRADING", "TRADING"),
        ("KIT_PLAN", "KIT_PLAN"),
        ("CO_FOUNDER", "CO_FOUNDER"),
    ]
    # User who did the transaction
    user = models.ForeignKey(
        'barter_auth.BarterUser',
        on_delete=models.PROTECT,
        related_name="withdrawals",
        verbose_name="Usuario",
    )
    # Wallet address of the client
    wallet_address = models.CharField(
        max_length=255, verbose_name="Dirección de billetera"
    )
    # Wallet provider
    wallet_provider = models.CharField(
        max_length=255,
        choices=Transaction.TRANSACTION_WALLET,
        verbose_name="Proveedor de billetera",
    )
    # in case that wallet provider is other we need to specify the provider
    other_wallet_provider = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Otro proveedor de billetera",
    )
    # Wallet network
    wallet_network = models.CharField(
        max_length=255, default="-", verbose_name="Red de billetera"
    )
    # Source of profit
    source_of_profit = models.CharField(
        max_length=255,
        choices=SOURCE_TYPE,
        default=SOURCE_TYPE[0][1],
        verbose_name="Tipo de retiro",
    )
    # transaction hash
    transaction_hash = models.CharField(
        max_length=250, blank=True, null=True, verbose_name="Hash de transacción"
    )
    # voucher screenshot
    voucher_screenshot = models.ImageField(
        upload_to="withdrawals/vouchers/",
        null=True,
        blank=True,
        verbose_name="Captura de voucher",
    )
    # confirmation screenshot
    confirmation_screenshot = models.ImageField(
        upload_to="withdrawals/confirmations/",
        null=True,
        blank=True,
        verbose_name="Captura de confirmación",
    )
    # Status of the transaction validated by the tech support staff
    transaction_status = models.IntegerField(
        choices=Transaction.TRANSACTION_STATUS, default=0, verbose_name="Estado"
    )
    # Amount paid in this transaction
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Monto")
    # fee transaction amount(is the 4% of the amount)
    fee_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="% Comisión por Retiro",
    )
    # amount after fee
    amount_after_fee = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Total pagado",
    )

    created_at = models.DateTimeField(default=now, verbose_name="Creado en")

    transaction_date = models.DateTimeField(
        default=now, verbose_name="Fecha de transacción"
    )

    @property
    def transaction_status_name(self):
        return Transaction.TRANSACTION_STATUS[self.transaction_status][1]

    class Meta:
        verbose_name = "Retiro"
        verbose_name_plural = "Retiros"

    def __str__(self):
        return f"{self.id} - {self.user.get_full_name()} - {self.amount}"


class MonthlyTradingEarnings(models.Model):
    MONTHS = [(i, calendar.month_name[i]) for i in range(1, 13)]
    # return of investment
    roi = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="ROI, omita el registro puesto que el sistema lo calcula.",
    )
    # month that the earnings are calculated (in integer)
    month = models.IntegerField(verbose_name="Mes", default=now().month, choices=MONTHS)
    # year that the earnings are calculated (in integer)
    year = models.IntegerField(verbose_name="Año", default=now().year)
    # created_at
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Creado en")

    class Meta:
        verbose_name = "Ganancia mensual de trading"
        verbose_name_plural = "Ganancias mensuales de trading"

    def __str__(self):
        return f"{self.month} - {self.year} - {self.roi}"


class MonthlyTradingEarningsPerLeader(models.Model):
    # create enum for the status of the transaction: pending, approved, rejected
    STATUS = [(0, "Pendiente"), (1, "Aprobado"), (2, "Rechazado")]

    # user that is the leader
    user = models.ForeignKey(
        'barter_auth.BarterUser', on_delete=models.PROTECT, related_name="monthly_trading_earnings"
    )

    # monthly trading earnings
    monthly_trading_earnings = models.ForeignKey(
        MonthlyTradingEarnings, on_delete=models.PROTECT, related_name="leaders"
    )
    # amount of earnings
    earnings = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Ganancias"
    )
    # earnings paid to the leader
    earnings_paid = models.DecimalField(
        max_digits=10, decimal_places=2, default=0, verbose_name="Ganancias pagadas"
    )
    # save calculation processes for manual review
    calculation_process = models.TextField(
        verbose_name="Procesos de calculo", blank=True, null=True
    )
    # status of the transaction
    status = models.IntegerField(choices=STATUS, default=0)
    # created_at
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Creado en")

    def __str__(self):
        return f"{self.user} - {self.earnings} - {self.monthly_trading_earnings}"

    class Meta:
        verbose_name = "Ganancia mensual de trading por líder"
        verbose_name_plural = "Ganancias mensuales de trading por líder"


class CoFounderEarningByTrading(models.Model):
    MONTHS = [(i, calendar.month_name[i]) for i in range(1, 13)]

    leadership_pool_type = models.ForeignKey(
        "global_settings.LeadershipPoolType",
        on_delete=models.PROTECT,
        related_name="cofounder_earnings_by_trading",
        null=tuple,
        verbose_name="Pool de liderazgo",
    )

    earning_percentage = models.DecimalField(
        max_digits=10,
        decimal_places=3,
        validators=[MinValueValidator(0), MaxValueValidator(1)],
        verbose_name="Porcentaje de ganancias",
    )

    month = models.IntegerField(verbose_name="Mes", default=now().month, choices=MONTHS)

    trimester = models.IntegerField(
        verbose_name="Trimestre (Auto)", null=True, blank=True
    )

    year = models.IntegerField(verbose_name="Año", default=now().year)

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Creado en")

    def __str__(self):
        return f"{self.id} - {self.leadership_pool_type.name} - {self.earning_percentage} - {self.month} - {self.year}"

    class Meta:
        verbose_name = "Ganancia de cofundador por trading"
        verbose_name_plural = "Ganancias de cofundador por trading"


class CoFounderEarningByProducts(models.Model):
    PRODUCTS = (
        [  # create enum for the products: dashboard, wallet, streaming, marketing
            (0, "Dashboard"),
            (1, "Wallet"),
            (2, "Streaming"),
            (3, "Marketing"),
        ]
    )
    MONTHS = [(i, calendar.month_name[i]) for i in range(1, 13)]

    leadership_pool_type = models.ForeignKey(
        "global_settings.LeadershipPoolType",
        on_delete=models.PROTECT,
        related_name="cofounder_earnings_by_products",
        null=True,
        verbose_name="Pool de liderazgo",
    )

    earning_percentage = models.DecimalField(
        max_digits=10,
        decimal_places=3,
        validators=[MinValueValidator(0), MaxValueValidator(1)],
        verbose_name="Porcentaje de ganancias",
    )

    product = models.IntegerField(choices=PRODUCTS, verbose_name="Producto")

    month = models.IntegerField(verbose_name="Mes", default=now().month, choices=MONTHS)

    trimester = models.IntegerField(
        verbose_name="Trimestre (Auto)", null=True, blank=True
    )

    year = models.IntegerField(verbose_name="Año", default=now().year)

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Creado en")

    def __str__(self):
        return f"{self.id} - {self.leadership_pool_type.name} - {self.earning_percentage} - {self.product} - {self.month} - {self.year}"

    class Meta:
        verbose_name = "Ganancia de cofundador por producto"
        verbose_name_plural = "Ganancias de cofundador por producto"


class DetailCoFounderEarningByTrading(models.Model):
    co_founder_earning_by_trading = models.ForeignKey(
        CoFounderEarningByTrading,
        on_delete=models.PROTECT,
        related_name="details",
        verbose_name="Ganancia de cofundador de trading",
    )

    user = models.ForeignKey(
        'barter_auth.BarterUser',
        on_delete=models.PROTECT,
        related_name="co_founder_earning_by_trading",
        verbose_name="Usuario",
    )

    earnings = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Ganancias"
    )

    earnings_paid = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Ganancias pagadas"
    )

    process = models.TextField(
        verbose_name="Procesos de calculo", blank=True, null=True
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Creado en")

    def __str__(self):
        return f"{self.co_founder_earning_by_trading} - {self.user} - {self.earnings}"

    class Meta:
        verbose_name = "Detalle de ganancia de cofundador por trading"
        verbose_name_plural = "Detalles de ganancia de cofundador por trading"


class DetailCoFounderEarningByProducts(models.Model):
    co_founder_earning_by_products = models.ForeignKey(
        CoFounderEarningByProducts,
        on_delete=models.PROTECT,
        related_name="details",
        verbose_name="Ganancia de cofundador por producto",
    )

    user = models.ForeignKey(
        'barter_auth.BarterUser',
        on_delete=models.PROTECT,
        related_name="co_founder_earning_by_products",
        verbose_name="Usuario",
    )

    earnings = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Ganancias"
    )

    earnings_paid = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Ganancias pagadas"
    )

    process = models.TextField(
        verbose_name="Procesos de calculo", blank=True, null=True
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Creado en")

    def __str__(self):
        return f"{self.co_founder_earning_by_products} - {self.user} - {self.earnings}"

    class Meta:
        verbose_name = "Detalle de ganancia de cofundador por producto"
        verbose_name_plural = "Detalles de ganancia de cofundador por producto"


class ReInvestments(models.Model):
    TYPE_RE_INVESTMENT = (
        [  # create enum for the products: dashboard, wallet, streaming, marketing
            ("Trading", "Trading"),
            ("Co-Founder", "Co-Founder"),
        ]
    )

    user = models.ForeignKey(
        'barter_auth.BarterUser',
        on_delete=models.PROTECT,
        related_name="re_investments",
        verbose_name="Usuario",
    )

    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Monto")

    type_re_investment = models.CharField(
        max_length=20, choices=TYPE_RE_INVESTMENT, verbose_name="Tipo de reinversión"
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Creado en")

    def __str__(self):
        return f"{self.user} - {self.amount}"

    class Meta:
        verbose_name = "Reinversión"
        verbose_name_plural = "Reinversiones"


# region Balance
class BalanceTransactionType(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Nombre")
    unique_code = models.CharField(
        max_length=5, unique=True, verbose_name="Código único para developers"
    )
    description = models.CharField(
        max_length=255, blank=True, verbose_name="Descripcion corta"
    )
    app_lookup = models.CharField(max_length=50, verbose_name="App del modelo")
    model_lookup = models.CharField(max_length=100, verbose_name="Nombre del modelo")
    balance_lookup_field = models.CharField(
        max_length=50, verbose_name="Columna de balance que modifica"
    )
    is_income = models.BooleanField(verbose_name="Es ingreso")

    enabled = models.BooleanField(default=True, verbose_name="Habilitado")
    created_at = models.DateTimeField(
        auto_now_add=True, blank=True, verbose_name="Creado en"
    )
    updated_at = models.DateTimeField(
        auto_now=True, blank=True, verbose_name="Modificado en"
    )

    class Meta:
        verbose_name = "Tipo de trasanccion en balance"
        verbose_name_plural = "Tipos de transaccion en balance"

    def __str__(self):
        return f"{self.id} - {self.name} - {self.balance_lookup_field}"


class Balance(models.Model):
    user = models.ForeignKey(
        'barter_auth.BarterUser',
        on_delete=models.PROTECT,
        related_name="balance",
        verbose_name="Usuario",
    )

    general_balance = models.DecimalField(
        max_digits=21,
        decimal_places=4,
        verbose_name="Balance general",
        default=0,
        help_text="Balance que el usuario puede utilizar para cualquier producto del dashboard",
    )
    cofounder_balance = models.DecimalField(
        max_digits=21, decimal_places=4, verbose_name="Balance de cofundador"
    )
    cofounder_earnings = models.DecimalField(
        max_digits=21, decimal_places=4, verbose_name="Ganancias de cofundador"
    )
    trading_balance = models.DecimalField(
        max_digits=21, decimal_places=4, verbose_name="Balance de trading"
    )
    trading_earnings = models.DecimalField(
        max_digits=21, decimal_places=4, verbose_name="Ganancias de trading personales"
    )
    trading_network_earnings = models.DecimalField(
        max_digits=21, decimal_places=4, verbose_name="Ganancias de trading de red"
    )
    kitplan_balance = models.DecimalField(
        max_digits=21, decimal_places=4, verbose_name="Balance de kitplan"
    )
    kitplan_network_earnings = models.DecimalField(
        max_digits=21, decimal_places=4, verbose_name="Ganancias de kitplan de red"
    )

    enabled = models.BooleanField(default=True, verbose_name="Habilitado")
    created_at = models.DateTimeField(
        auto_now_add=True, blank=True, verbose_name="Creado en"
    )
    updated_at = models.DateTimeField(
        auto_now=True, blank=True, verbose_name="Modificado en"
    )

    class Meta:
        verbose_name = "Balance"
        verbose_name_plural = "Balances"

    def __str__(self):
        return f"{self.id} - {self.user.id} - {self.user.first_name} {self.user.last_name} - {self.user.email}"


class BalanceHistory(models.Model):
    balance = models.ForeignKey(
        Balance,
        on_delete=models.PROTECT,
        related_name="history",
        verbose_name="Balance",
    )
    balance_transaction_type = models.ForeignKey(
        BalanceTransactionType,
        on_delete=models.PROTECT,
        related_name="balance_history",
        verbose_name="Tipo de transaccion en balance",
    )
    object_id = models.BigIntegerField(verbose_name="Id de objeto")
    object_date = models.DateTimeField(verbose_name="Fecha de transaccion de objeto")
    amount = models.DecimalField(
        max_digits=21, decimal_places=4, verbose_name="Monto de transaccion"
    )

    enabled = models.BooleanField(default=True, verbose_name="Habilitado")
    created_at = models.DateTimeField(
        auto_now_add=True, blank=True, verbose_name="Creado en"
    )
    updated_at = models.DateTimeField(
        auto_now=True, blank=True, verbose_name="Modificado en"
    )

    class Meta:
        verbose_name = "Historial de balance"
        verbose_name_plural = "Historial de balances"

    def __str__(self):
        return f"{self.id} - {self.amount} - {self.balance.user.first_name} {self.balance.user.last_name}"


# endregion


class KitPlanNetWorkEarnings(models.Model):
    unilevel_network = models.ForeignKey(
        'barter_auth.UnilevelNetwork',
        on_delete=models.PROTECT,
        related_name="kitplan_network_earnings",
        verbose_name="Red de referidos de Kit Plan",
    )
    kit_plan_unilevel_network = models.ForeignKey(
        'global_settings.KitPlanUnilevelPercentage',
        on_delete=models.PROTECT,
        related_name="kitplan_network_earnings",
        verbose_name="Porcentaje de red de referidos de Kit Plan",
    )
    level = models.PositiveIntegerField(verbose_name="Nivel")
    level_earnings_percentage = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Porcentaje de ganancias de nivel"
    )
    transaction = models.ForeignKey(
        Transaction,
        on_delete=models.PROTECT,
        related_name="kitplan_network_earnings",
        verbose_name="Transaccion",
    )
    current_investment = models.DecimalField(
        max_digits=21, decimal_places=4, verbose_name="Inversion actual"
    )

    earnings = models.DecimalField(
        max_digits=21, decimal_places=4, verbose_name="Ganancias"
    )

    calculation_process = models.TextField(
        verbose_name="Proceso de calculo", blank=True, null=True
    )

    enabled = models.BooleanField(default=True, verbose_name="Habilitado")
    created_at = models.DateTimeField(
        auto_now_add=True, blank=True, verbose_name="Creado en"
    )
    updated_at = models.DateTimeField(
        auto_now=True, blank=True, verbose_name="Modificado en"
    )

    @property
    def user_network(self):
        return self.unilevel_network.user

    @property
    def user_in_network(self):
        return self.unilevel_network.user_in_network

    class Meta:
        verbose_name = "Red de referidos de Kit Plan(Ganancias)"
        verbose_name_plural = "Red de referidos de Kit Plan(Ganancias)"

    def __str__(self):
        return f"{self.id} - {self.current_investment} - {self.level} Level - {self.earnings}"


class TradingEarnings(models.Model):
    # usuario
    user = models.ForeignKey('barter_auth.BarterUser', on_delete=models.PROTECT, related_name='trading_earnings',
                             verbose_name='Usuario')
    # porcentaje de ganancias
    trading_percentage = models.ForeignKey(MonthlyTradingEarnings, on_delete=models.PROTECT,
                                           related_name='trading_earnings',
                                           verbose_name='Porcentaje de ganancias')
    # porcentaje de ganancia usado
    trading_percentage_used = models.DecimalField(max_digits=10, decimal_places=2,
                                                  verbose_name='Porcentaje de ganancia usado')
    # transacción
    transaction = models.ForeignKey(Transaction, on_delete=models.PROTECT, related_name='trading_earnings',
                                    verbose_name='Transacción', null=True, blank=True)
    # re-inversion
    reinvestment = models.ForeignKey(ReInvestments, on_delete=models.PROTECT, related_name='trading_earnings',
                                     verbose_name='Re-inversion', null=True, blank=True)

    # inversion actual
    current_investment = models.DecimalField(max_digits=21, decimal_places=4, verbose_name='Inversion actual')
    # ganancias
    earnings = models.DecimalField(max_digits=21, decimal_places=4, verbose_name='Ganancias')
    # proceso de calculo
    calculation_process = models.TextField(verbose_name='Proceso de calculo', blank=True, null=True)

    calculated_earnings = models.BooleanField(default=False, verbose_name='Ganancias calculadas', blank=True, null=True)

    enabled = models.BooleanField(default=True, verbose_name='Habilitado')
    created_at = models.DateTimeField(auto_now_add=True, blank=True, verbose_name='Creado en')
    updated_at = models.DateTimeField(auto_now=True, blank=True, verbose_name='Modificado en')

    class Meta:
        verbose_name = 'Ganancias de Trading'
        verbose_name_plural = 'Ganancias de Trading'

    def __str__(self):
        return f'{self.id} - {self.current_investment} - {self.earnings}'

    @property
    def type_earning(self):
        return f'Inversion #{self.transaction.id}' if self.transaction else f'Re-inversion #{self.reinvestment.id}'


class TradingNetWorkEarnings(models.Model):
    unilevel_network = models.ForeignKey('barter_auth.UnilevelNetwork', on_delete=models.PROTECT,
                                         related_name='trading_network_earnings',
                                         verbose_name='Red de referidos de Trading')
    trading_unilevel_network = models.ForeignKey('global_settings.TradingUnilevelPercentage', on_delete=models.PROTECT,
                                                 related_name='trading_network_earnings',
                                                 verbose_name='Porcentaje de red de referidos de Trading')

    trading_percentage = models.ForeignKey(MonthlyTradingEarnings, on_delete=models.PROTECT,
                                           related_name='trading_netow_earnings',
                                           verbose_name='Porcentaje de ganancias', blank=True, null=True)
    trading_earnings = models.ForeignKey(TradingEarnings, on_delete=models.PROTECT,
                                         related_name='trading_network_earnings',
                                         verbose_name='Ganancias de Trading', blank=True, null=True)
    level = models.PositiveIntegerField(verbose_name='Nivel')
    level_earnings_percentage = models.DecimalField(max_digits=10, decimal_places=2,
                                                    verbose_name='Porcentaje de ganancias de nivel')

    current_investment = models.DecimalField(max_digits=21, decimal_places=4, verbose_name='Inversion actual')
    earnings = models.DecimalField(max_digits=21, decimal_places=4, verbose_name='Ganancias')
    calculation_process = models.TextField(verbose_name='Proceso de calculo', blank=True, null=True)

    enabled = models.BooleanField(default=True, verbose_name='Habilitado')

    created_at = models.DateTimeField(auto_now_add=True, blank=True, verbose_name='Creado en')
    updated_at = models.DateTimeField(auto_now=True, blank=True, verbose_name='Modificado en')

    @property
    def user_network(self):
        return self.unilevel_network.user

    @property
    def user_in_network(self):
        return self.unilevel_network.user_in_network

    class Meta:
        verbose_name = 'Red de referidos de Trading(Ganancias)'
        verbose_name_plural = 'Red de referidos de Trading(Ganancias)'

    def __str__(self):
        return f'{self.id} - {self.current_investment} - {self.level} Level - {self.earnings}'


# region Deprecated models
# ! Should't be used anymore, cant be deleted due to data in the database
# TODO: Backup data and remove models


class DailyPercentageRevenue(models.Model):
    """
    This model was used to store the daily percentage to be used
    to calculate an user's daily trading revenue
    Deprecated in favor of monthly percentages
    """

    date = models.DateField(unique=True)
    percentage_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(0.88)],
    )

    enabled = models.BooleanField(default=True, verbose_name="Habilitado")
    created_at = models.DateTimeField(
        auto_now_add=True, blank=True, verbose_name="Creado en"
    )
    updated_at = models.DateTimeField(
        auto_now=True, blank=True, verbose_name="Modificado en"
    )

    class Meta:
        """
        Django admin display name
        """

        verbose_name = "Porcentaje de ganancia diario de trading"
        verbose_name_plural = "Porcentajes de ganancia diarios de trading"

    def __str__(self):
        return f"{self.date.strftime('%Y-%m-%d')} - {self.percentage_amount}"


class CumulativeRevenue(models.Model):
    """This model was used as a way to display an user's balance."""

    MONTHS = [(i, calendar.month_name[i]) for i in range(1, 13)]
    user = models.ForeignKey(
        'barter_auth.BarterUser',
        on_delete=models.PROTECT,
        related_name="cumulative_revenues",
        verbose_name="Usuario",
    )
    total_earnings = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Ganancias totales"
    )
    total_to_withdraw = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Total a retirar"
    )
    month = models.IntegerField(verbose_name="Mes", default=now().month, choices=MONTHS)
    year = models.IntegerField(verbose_name="Año", default=now().year)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Creado en")

    class Meta:
        """Django admin display name."""

        verbose_name = "Ganancia acumulada de usuario"
        verbose_name_plural = "Ganancias acumuladas de usuarios"

    def __str__(self):
        return f"{self.user}, {self.total_earnings}"


class UserDailyTradingRevenue(models.Model):
    """Model used to store daily revenue per transaction."""

    user = models.ForeignKey(
        'barter_auth.BarterUser',
        on_delete=models.PROTECT,
        related_name="earnings",
        verbose_name="Usuario",
    )
    daily_percentage_revenue = models.ForeignKey(
        DailyPercentageRevenue,
        on_delete=models.PROTECT,
        related_name="users_daily_trading_revenues",
        verbose_name="Porcentaje de ganancia",
    )
    transaction = models.ForeignKey(
        Transaction,
        on_delete=models.PROTECT,
        related_name="daily_earnings",
        null=True,
        blank=True,
        verbose_name="Transaccion de trading",
    )
    reinvestment = models.ForeignKey(
        "ReInvestments",
        on_delete=models.PROTECT,
        related_name="daily_trading_earnings",
        null=True,
        blank=True,
        verbose_name="Reinversion",
    )
    cumulative_revenue = models.ForeignKey(
        "CumulativeRevenue",
        on_delete=models.PROTECT,
        related_name="details",
        null=True,
        blank=True,
        verbose_name="Ganancia acumulada",
    )

    current_investment = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Inversion en el momento"
    )
    earnings_percentage = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Porcentaje de Ganancias"
    )
    earnings = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Ganancias"
    )
    earnings_date = models.DateField(verbose_name="Fecha")

    calculated_earnings = models.BooleanField(
        default=False, verbose_name="Ganancias de red calculadas", blank=True, null=True
    )

    enabled = models.BooleanField(default=True, verbose_name="Habilitado")
    created_at = models.DateTimeField(
        auto_now_add=True, blank=True, verbose_name="Creado en"
    )
    updated_at = models.DateTimeField(
        auto_now=True, blank=True, verbose_name="Modificado en"
    )

    class Meta:
        """Django admin display name."""

        verbose_name = "Ganancia diaria de trading de usuario"
        verbose_name_plural = "Ganancias diarias de trading de usuarios"

    def __str__(self):
        return f"{self.id} {self.user}, {self.earnings} - {self.earnings_date}"


# endregion