import calendar
import datetime

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from barter_auth.enums import TokenTypesEnum
from barter_auth.managers import CustomUserManager
from barter_auth.utils import generate_default_image, generate_referral_code
from global_settings.models import BlockchainChoices, ExchangeChoices
from kyc_verifications.models import KYCVerificationResult
from transactions.utils.user_balance_utils import (
    get_user_current_cofounder_balance,
    get_user_current_cofounder_earnings,
    get_user_current_kitplan_balance,
    get_user_current_kitplan_earnings,
    get_user_current_trading_balance,
    get_user_current_trading_earnings,
    get_count_users_direct,
)


def add_years(initial_date: datetime.datetime, years: int):
    try:
        return initial_date.replace(year=initial_date.year + years)
    except ValueError:
        return initial_date.replace(year=initial_date.year + years, day=28)


class BarterUser(AbstractUser):
    email = models.EmailField(_("email address"), unique=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    country = models.CharField(
        max_length=50, null=True, blank=True, verbose_name="Pais"
    )
    zip_code = models.CharField(
        max_length=10, null=True, blank=True, verbose_name="Codigo Postal"
    )
    phone_number = models.CharField(
        max_length=25, null=True, blank=True, verbose_name="Teléfono"
    )
    profile_image = models.URLField(
        default=generate_default_image, verbose_name="Imagen de perfil"
    )
    address = models.CharField(
        max_length=250, null=True, blank=True, verbose_name="Direccion"
    )
    city = models.CharField(max_length=50, null=True, blank=True, verbose_name="Ciudad")
    referral_code = models.CharField(
        max_length=250,
        null=True,
        blank=True,
        default=generate_referral_code,
        unique=True,
        verbose_name="Codigo de referido",
    )

    referred_by = models.ForeignKey(
        "self",
        on_delete=models.PROTECT,
        related_name="referrals",
        null=True,
        blank=True,
        verbose_name="Referido por",
    )

    verified = models.BooleanField(default=False, verbose_name="Verificado")

    is_co_founder = models.BooleanField(default=False, verbose_name="Es cofundador")
    leadership_pool_type = models.ForeignKey(
        "global_settings.LeadershipPoolType",
        on_delete=models.PROTECT,
        related_name="users",
        null=True,
        blank=True,
        verbose_name="Pool de liderazgo",
    )

    # region KYC Properties
    can_fill_kyc = models.BooleanField(default=True, verbose_name="Puede rellenar KYC")

    @property
    def has_kyc(self) -> bool:
        return (
            KYCVerificationResult.objects.filter(
                external_user_id=str(self.id),
                review_status="completed",
                review_result__review_answer="GREEN",
            ).count()
            > 0
            or self.kyc_manual_verification_details.filter(
                review_answer="GREEN"
            ).count()
            > 0
        )

    # endregion

    # region Kit Plan Properties
    @property
    def has_active_kitplan(self):
        one_year_ago = timezone.now() - datetime.timedelta(days=365)

        return self.transactions.filter(
            transaction_type="kit-plan",
            wallet_deposit_date__gte=one_year_ago,
            transaction_status=1,
        ).exists()

    @property
    def has_pending_kitplan_transaction(self):
        return self.transactions.filter(
            transaction_type="kit-plan", transaction_status=0
        ).exists()

    # endregion

    # region Admin Balance Properties

    # Do not use these properties anywhere else
    # as they are temporary
    # --Jeff

    @property
    def user_count_direct_users(self):
        return get_count_users_direct(self)

    user_count_direct_users.fget.short_description = "Cantidad de usuarios directos"

    @property
    def user_trading_balance_admin(self):
        return get_user_current_trading_balance(self)

    user_trading_balance_admin.fget.short_description = "Balance de trading actual"

    @property
    def user_trading_earnings_balance_admin(self):
        personal, red, total = get_user_current_trading_earnings(self)

        return f"""Ganancias actuales personales: {personal}
        Ganancias actuales de red: {red}
        Ganancias actuales totales: {total}"""

    user_trading_earnings_balance_admin.fget.short_description = (
        "Ganancias de trading actuales"
    )

    @property
    def user_kitplan_balance_admin(self):
        return get_user_current_kitplan_balance(self)

    user_kitplan_balance_admin.fget.short_description = "Balance de kit plan actual"

    @property
    def user_kitplan_network_earning_admin(self):
        return get_user_current_kitplan_earnings(self)

    user_kitplan_network_earning_admin.fget.short_description = (
        "Ganancias de red de kit plan actuales"
    )

    @property
    def user_cofounder_balance_admin(self):
        return get_user_current_cofounder_balance(self)

    user_cofounder_balance_admin.fget.short_description = "Balance de cofundador actual"

    @property
    def user_cofounder_balance_earnings_admin(self):
        productos, trading, total = get_user_current_cofounder_earnings(self)

        return f"""Ganancias por producto actuales: {productos}
        Ganancias por trading actuales: {trading}
        Ganancias actuales totales: {total}"""

    user_cofounder_balance_earnings_admin.fget.short_description = (
        "Ganancias de cofundador actuales"
    )

    # endregion

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def has_plan(self) -> bool:
        return self.plans.all().count() > 0

    # ! TODO: Remove completely in the future once frontend removes legacy code
    @property
    def profile_registered(self) -> bool:
        return True

    @property
    def has_trading_plan(self) -> bool:
        return self.bartertradingplan_set.all().count() > 0

    @property
    def has_network(self) -> bool:
        return self.branch.all().count() > 0

    @property
    def referral_link(self):
        return f"https://bartercapital-dashboard.com/#/auth/register?referral_code={self.referral_code}"

    @property
    def has_sales_funnel(self) -> bool:
        return self.sales_funnel.filter(enabled=True).count() > 0

    def __str__(self) -> str:
        return self.get_full_name()


class UnilevelNetwork(models.Model):
    user = models.ForeignKey(
        BarterUser,
        on_delete=models.PROTECT,
        related_name="unilevel_network",
        verbose_name="Red de",
    )
    user_in_network = models.ForeignKey(
        BarterUser,
        on_delete=models.PROTECT,
        related_name="unilevel_network_in",
        verbose_name="Usuario en red",
    )
    in_network_through = models.ForeignKey(
        BarterUser,
        on_delete=models.PROTECT,
        related_name="unilevel_network_users_through",
        verbose_name="A traves de",
    )  # Should never be user nor shown, just as reference
    level = models.PositiveIntegerField(verbose_name="Nivel")

    class Meta:
        verbose_name = "Red de usuario"
        verbose_name_plural = "Redes de usuarios"

    def __str__(self):
        return f"Red de {self.user} - {self.user_in_network}"


class BarterPlan(models.Model):
    PLANS_CHOICES = [
        (20, "$20"),
        (50, "$50"),
        (100, "$100"),
        (200, "$200"),
        (400, "$400"),
        (800, "$800"),
        (1000, "$1000"),
    ]
    user = models.ForeignKey(
        BarterUser,
        on_delete=models.PROTECT,
        related_name="plans",
        verbose_name="Usuario",
    )
    selected_plan = models.PositiveSmallIntegerField(
        choices=PLANS_CHOICES, default=20, verbose_name="Plan seleccionado"
    )
    transaction = models.ForeignKey(
        "transactions.Transaction",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        verbose_name="Transacción",
        related_name="kit_plans",
    )
    plan = models.ForeignKey(
        "global_settings.KitPlan",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        verbose_name="Plan",
        related_name="kit_plans",
    )
    transaction_hash = models.CharField(
        max_length=250, verbose_name="Hash de transacción"
    )
    cap_reached = models.BooleanField(
        default=False, verbose_name="Tope alcanzado", null=True, blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def expiration(self) -> datetime.datetime:
        return add_years(self.created_at, 1)

    @property
    def yearly_revenue(self):
        return self.selected_plan * 3

    @property
    def credentials(self):
        return self.credentials.all()

    def __str__(self):
        return f"{self.user.get_full_name()}  ${self.selected_plan}"

    class Meta:
        verbose_name = "Compra de Kit plan"
        verbose_name_plural = "Compras de Kit plans"


class BarterPlanCredentials(models.Model):
    plan = models.ForeignKey(
        BarterPlan,
        on_delete=models.PROTECT,
        related_name="credentials",
        verbose_name="Plan",
    )
    description = models.CharField(max_length=250, verbose_name="Plataforma")
    username = models.CharField(max_length=250, verbose_name="Usuario")
    password = models.CharField(max_length=250, verbose_name="Clave")
    created_at = models.DateTimeField(auto_now_add=True)
    start_date = models.DateField(verbose_name="Fecha de inicio")
    end_date = models.DateField(verbose_name="Fecha de finalización")

    class Meta:
        verbose_name = "Credencial de Kit Plan"
        verbose_name_plural = "Credenciales de Kit Plans"

    def __str__(self):
        return f"{self.plan.user.get_full_name()} - ${self.plan.selected_plan} plan credentials"


class BarterTradingPlan(models.Model):
    user = models.ForeignKey(
        BarterUser, on_delete=models.PROTECT, verbose_name="Usuario"
    )
    trading_amount = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Inversión"
    )
    transaction_hash = models.CharField(
        max_length=250, verbose_name="Hash de transacción"
    )
    transaction = models.ForeignKey(
        "transactions.Transaction",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        verbose_name="Transacción",
        related_name="trading_plans",
    )
    plan = models.ForeignKey(
        "global_settings.TradingPlans",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        verbose_name="Plan",
        related_name="trading_plans",
    )
    cap_reached = models.BooleanField(
        default=False, verbose_name="Tope alcanzado", null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.get_full_name()} ${self.trading_amount}"

    class Meta:
        verbose_name = "Inversion de trading"
        verbose_name_plural = "Inversiones de trading"


class VerificationActions(models.Model):
    user = models.ForeignKey(BarterUser, on_delete=models.CASCADE)
    token = models.BinaryField()
    used = models.BooleanField(default=False)
    type = models.IntegerField(
        choices=TokenTypesEnum.choices, default=TokenTypesEnum.VERIFICATION.value
    )
    expiration_date = models.DateTimeField(null=False)

    def __str__(self) -> str:
        return f"{self.user.username} for {TokenTypesEnum(self.type).label}"


class UserWallet(models.Model):
    user = models.ForeignKey(
        BarterUser,
        on_delete=models.PROTECT,
        related_name="wallet",
        verbose_name="Usuario",
    )
    hash = models.CharField(
        max_length=40, unique=True, verbose_name="Hash de la billetera"
    )
    blockchain = models.ForeignKey(
        BlockchainChoices,
        on_delete=models.PROTECT,
        related_name="business_user",
        verbose_name="Blockchain",
    )
    exchange = models.ForeignKey(
        ExchangeChoices,
        on_delete=models.PROTECT,
        related_name="business_user",
        verbose_name="Red/Moneda",
    )
    enabled = models.BooleanField(verbose_name="Habilitado", default=True)

    class Meta:
        verbose_name = "Billetera de Usuario"
        verbose_name_plural = "Billeteras de Usuario"

    def __str__(self) -> str:
        return f"{self.user.get_full_name()} [ {self.blockchain} | {self.exchange} ]{self.hash}"


# region Deprecated models
# ! Do not delete them as they hold database information
# ! Unless a backup is made and stored somewhere in the cloud


class BarterUserSecurityProfile(models.Model):
    user: BarterUser = models.ForeignKey(
        BarterUser,
        on_delete=models.PROTECT,
        related_name="security_profiles",
        verbose_name="Usuario",
    )
    dni_image = models.CharField(
        max_length=250, null=True, blank=True, verbose_name="Imagen DNI frontal"
    )
    dni_back_image = models.CharField(
        max_length=250, null=True, blank=True, verbose_name="Imagen DNI reverso"
    )
    terms_and_conditions = models.BooleanField(
        default=False, verbose_name="Acepto terminos y condiciones"
    )

    def __str__(self) -> str:
        return self.user.get_full_name()

    class Meta:
        verbose_name = "Perfil de seguridad"
        verbose_name_plural = "Perfiles de seguridad"


class Referral(models.Model):
    CATEGORY_OPTIONS = [("child", "Kid Account"), ("common", "Common Account")]

    user = models.ForeignKey(
        "BarterUser", on_delete=models.PROTECT, related_name="branch"
    )
    investment = models.ForeignKey(
        "BarterUser", on_delete=models.PROTECT, related_name="leader"
    )
    transaction_hash = models.CharField(max_length=250, blank=True, default="-")
    amount = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True, default=0.0
    )
    category = models.CharField(max_length=250, choices=CATEGORY_OPTIONS)

    def get_leader(self):
        return self.user

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"


class BarterUserNode(models.Model):
    CATEGORY_OPTIONS = [("child", "Kid Account"), ("common", "Common Account")]

    NODE_LEVELS = [
        (1, "Level 1"),
        (2, "Level 2"),
        (3, "Level 3"),
        (4, "Level 4"),
        (5, "Level 5"),
        (6, "Level 6"),
        (7, "Level 7"),
        (8, "Level 8"),
        (9, "Level 9"),
        (10, "Level 10"),
    ]

    user = models.ForeignKey(
        "BarterUser", on_delete=models.PROTECT, related_name="node_branch"
    )
    investment = models.ForeignKey(
        "BarterUser", on_delete=models.PROTECT, related_name="node_leader"
    )
    category = models.CharField(max_length=250, choices=CATEGORY_OPTIONS)
    reference_code = models.CharField(max_length=250)
    node_level = models.IntegerField(choices=NODE_LEVELS, default=NODE_LEVELS[0][0])

    def __str__(self):
        return f"{self.user.username} - {self.investment.username} Level: {self.node_level}"

    class Meta:
        verbose_name = "Referido"
        verbose_name_plural = "Referidos"


class PlansEarnings(models.Model):
    STATUS = [(0, "Pendiente"), (1, "Aprobado"), (2, "Rechazado")]
    MONTHS = [(i, calendar.month_name[i]) for i in range(1, 13)]

    user = models.ForeignKey(
        BarterUser, on_delete=models.CASCADE, related_name="plans_earnings"
    )
    earning = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Ganancia", default=0
    )
    earning_paid = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Ganancia pagada", default=0
    )
    month = models.IntegerField(
        choices=MONTHS, verbose_name="Mes", null=True, blank=True
    )
    year = models.IntegerField(verbose_name="Año", null=True, blank=True)
    # crear signal que cuando el estado cambie a aprobado el earning_paid se actualice
    status = models.IntegerField(choices=STATUS, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Ganancia de Kit Plan por Líder"
        verbose_name_plural = "Ganancias de Kit Plan por Líder"

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.earning}"


class PlansEarningsDetail(models.Model):
    plan_earning = models.ForeignKey(
        PlansEarnings,
        on_delete=models.CASCADE,
        related_name="details",
        verbose_name="Ganancia de plan",
    )
    earning = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Ganancia"
    )
    calculation_process = models.TextField(
        verbose_name="Procesos de calculo", blank=True, null=True
    )
    transaction = models.ForeignKey(
        "transactions.Transaction",
        on_delete=models.CASCADE,
        related_name="plan_earning_details",
        null=True,
        blank=True,
        verbose_name="Transacción",
    )
    level = models.IntegerField(verbose_name="Nivel", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Detalle de las ganancias de Kit Plan por Líder"
        verbose_name_plural = "Detalles de las ganancias de Kit Plan por Líder"

    def __str__(self):
        return f"{self.plan_earning.user.get_full_name()} - {self.plan_earning.earning}"


# endregion
