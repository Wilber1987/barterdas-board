from django.core.validators import (
    MinValueValidator,
    MaxValueValidator,
    FileExtensionValidator,
)
from django.db import models

from .custom_storage import QRCodeStorage


def get_qr_filename(instance, filename):
    ext = filename.split(".")[-1]
    filename = f"{instance.hash}.{ext}"
    return filename


class WithdrawalType(models.Model):
    description = models.CharField(
        max_length=100, unique=True, verbose_name="Descripcion"
    )
    value = models.PositiveSmallIntegerField(unique=True, verbose_name="Valor")
    enabled = models.BooleanField(verbose_name="Habilitado")

    class Meta:
        verbose_name = "Tipo de retiros"
        verbose_name_plural = "Tipos de retiros"


class KitPlanCategory(models.Model):
    name = models.CharField(max_length=30, unique=True, verbose_name="Titulo")
    description = models.CharField(
        max_length=255, blank=True, verbose_name="Descripcion"
    )

    enabled = models.BooleanField(verbose_name="Habilitado")
    created_at = models.DateTimeField(
        auto_now_add=True, blank=True, verbose_name="Creado en"
    )
    updated_at = models.DateTimeField(
        auto_now=True, blank=True, verbose_name="Modificado en"
    )

    class Meta:
        verbose_name = "Categorias de Kit Plan"
        verbose_name_plural = "Categorias de Kit Plan"

    def __str__(self):
        return f"{self.id} - {self.name}"


class KitPlan(models.Model):
    kit_plan_category = models.ForeignKey(
        KitPlanCategory,
        on_delete=models.PROTECT,
        related_name="kit_plans",
        null=True,
        verbose_name="Categoria",
    )
    title = models.CharField(max_length=100, unique=True, verbose_name="Titulo")
    short_description = models.CharField(
        max_length=100, blank=True, verbose_name="Descripcion corta"
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name="Precio",
    )
    business_volume = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Volumen de negocio"
    )
    earnings_cap = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Techo de ganancias"
    )
    allow_repurchase = models.BooleanField(verbose_name="Permitir recompra")
    can_be_upgraded = models.BooleanField(verbose_name="Permitir subir de plan")

    enabled = models.BooleanField(verbose_name="Habilitado")
    created_at = models.DateTimeField(
        auto_now_add=True, blank=True, verbose_name="Creado en"
    )
    updated_at = models.DateTimeField(
        auto_now=True, blank=True, verbose_name="Modificado en"
    )

    class Meta:
        verbose_name = "Kit Plan"
        verbose_name_plural = "Kit Plans"

    def __str__(self):
        return f"{self.id} - {self.title} - ${self.price}"


class KitPlanDetail(models.Model):
    kit_plan = models.ForeignKey(
        KitPlan,
        on_delete=models.PROTECT,
        related_name="details",
        verbose_name="Kit Plan",
    )
    position = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0)], verbose_name="Posicion"
    )
    description = models.CharField(max_length=100, verbose_name="Descripcion")

    created_at = models.DateTimeField(
        auto_now_add=True, blank=True, verbose_name="Creado en"
    )
    updated_at = models.DateTimeField(
        auto_now=True, blank=True, verbose_name="Modificado en"
    )

    class Meta:
        verbose_name = "Detalle de Kit Plan"
        verbose_name_plural = "Detalles de Kit Plan"

    def __str__(self):
        return f"{self.id}-{self.kit_plan.id} {self.description}"


class BlockchainChoices(models.Model):
    name = models.CharField(max_length=20, verbose_name="Nombre")

    class Meta:
        verbose_name = "Blockchain"
        verbose_name_plural = "Blockchains"

    def __str__(self) -> str:
        return f"{self.name}"


class ExchangeChoices(models.Model):
    name = models.CharField(max_length=20, verbose_name="Nombre")

    class Meta:
        verbose_name = "Exchange"
        verbose_name_plural = "Exchanges"

    def __str__(self) -> str:
        return f"{self.name}"


class CryptocurrencyChoices(models.Model):
    name = models.CharField(max_length=50, verbose_name="Nombre")

    class Meta:
        verbose_name = "Criptomoneda"
        verbose_name_plural = "Criptomonedas"

    def __str__(self):
        return f"{self.name}"


class BusinessWalletType(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nombre")
    description = models.TextField(blank=True, verbose_name="Descripción")

    enabled = models.BooleanField(verbose_name="Habilitado")
    created_at = models.DateTimeField(
        auto_now_add=True, blank=True, verbose_name="Creado en"
    )
    updated_at = models.DateTimeField(
        auto_now=True, blank=True, verbose_name="Modificado en"
    )

    class Meta:
        verbose_name = "Tipo de Billeteras de empresa"
        verbose_name_plural = "Tipos de Billeteras de empresa"

    def __str__(self) -> str:
        return self.name


class BusinessWallet(models.Model):
    hash = models.CharField(max_length=255, verbose_name="Hash de la billetera")
    qr_code = models.ImageField(
        blank=True,
        upload_to=get_qr_filename,
        storage=QRCodeStorage(),
        validators=[FileExtensionValidator(["jpg", "png", "jpeg", "webp"])],
        verbose_name="Codigo QR",
    )
    blockchain = models.ForeignKey(
        BlockchainChoices,
        on_delete=models.PROTECT,
        related_name="business_wallets",
        verbose_name="Blockchain",
    )
    exchange = models.ForeignKey(
        ExchangeChoices,
        on_delete=models.PROTECT,
        related_name="business_wallets",
        verbose_name="Exchange",
    )
    cryptocurrency = models.ForeignKey(
        CryptocurrencyChoices,
        on_delete=models.PROTECT,
        related_name="business_wallets",
        verbose_name="Criptomoneda",
        null=True,
    )
    type = models.ForeignKey(
        BusinessWalletType,
        null=True,
        on_delete=models.PROTECT,
        related_name="wallets",
        verbose_name="Tipo de billetera",
    )
    enabled = models.BooleanField(default=True, verbose_name="Habilitado")

    class Meta:
        verbose_name = "Billetera de empresa"
        verbose_name_plural = "Billeteras de empresa"

    def __str__(self) -> str:
        return f"[ {self.exchange} | {self.blockchain} | {self.cryptocurrency} ] {self.hash}"


class LeadershipPoolType(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Nombre")
    description = models.CharField(
        max_length=100, blank=True, verbose_name="Descripcion"
    )
    earning_percentage = models.DecimalField(
        max_digits=6,
        decimal_places=3,
        validators=[MinValueValidator(0.00), MaxValueValidator(1.0)],
        verbose_name="Porcentaje de ganancia",
    )

    enabled = models.BooleanField(verbose_name="Habilitado")
    created_at = models.DateTimeField(
        auto_now_add=True, blank=True, verbose_name="Creado en"
    )
    updated_at = models.DateTimeField(
        auto_now=True, blank=True, verbose_name="Modificado en"
    )

    class Meta:
        verbose_name = "Pool de liderazgo"
        verbose_name_plural = "Pools de liderazgo"

    def __str__(self):
        return f"{self.id} - {self.name}"


class KitPlanUnilevelPercentage(models.Model):
    name = models.CharField(max_length=20, unique=True, verbose_name="Nombre")
    description = models.CharField(
        max_length=100, blank=True, verbose_name="Descripcion"
    )
    level = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)], verbose_name="Nivel"
    )
    earnings_percentage = models.DecimalField(
        max_digits=6,
        decimal_places=3,
        validators=[MinValueValidator(0), MaxValueValidator(1)],
        verbose_name="Porcentaje de ganancia de nivel",
    )
    kit_plan = models.ForeignKey(
        KitPlan,
        on_delete=models.PROTECT,
        related_name="unilevel_percentages",
        verbose_name="Kit Plan",
        null=True,
        blank=True,
    )  # TODO: Eliminar null y blank
    enabled = models.BooleanField(verbose_name="Habilitado")
    created_at = models.DateTimeField(
        auto_now_add=True, blank=True, verbose_name="Creado en"
    )
    updated_at = models.DateTimeField(
        auto_now=True, blank=True, verbose_name="Modificado en"
    )

    class Meta:
        verbose_name = "Porcentaje de ganancia por nivel de Kit Plan"
        verbose_name_plural = "Porcentajes de ganancia por nivel de Kit Plan"

    def __str__(self):
        return (
            f"{self.id} - {self.name} - Nivel {self.level} - {self.earnings_percentage}"
        )


class TradingPlans(models.Model):
    code = models.CharField(max_length=255, verbose_name="Codigo del plan")
    name = models.CharField(max_length=255, verbose_name="Nombre del plan")
    description = models.TextField(verbose_name="Descripcion del plan")
    price = models.DecimalField(
        max_digits=21, decimal_places=4, verbose_name="Monto del plan"
    )
    cap = models.DecimalField(
        max_digits=21, decimal_places=4, verbose_name="Tope del plan (%)"
    )

    enabled = models.BooleanField(default=True, verbose_name="Habilitado")
    created_at = models.DateTimeField(
        auto_now_add=True, blank=True, verbose_name="Creado en"
    )
    updated_at = models.DateTimeField(
        auto_now=True, blank=True, verbose_name="Modificado en"
    )

    def __str__(self):
        return f"{self.id} - {self.name}"

    class Meta:
        verbose_name = "Plan de Trading"
        verbose_name_plural = "Planes de Trading"


class TradingUnilevelPercentage(models.Model):
    name = models.CharField(max_length=20, unique=True, verbose_name="Nombre")
    description = models.CharField(
        max_length=100, blank=True, verbose_name="Descripcion"
    )
    level = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)], verbose_name="Nivel"
    )
    earnings_percentage = models.DecimalField(
        max_digits=6,
        decimal_places=3,
        validators=[MinValueValidator(0), MaxValueValidator(1)],
        verbose_name="Porcentaje de ganancia de nivel",
    )
    trading_plan = models.ForeignKey(
        TradingPlans,
        on_delete=models.PROTECT,
        related_name="trading_unilevel_percentages",
        verbose_name="Plan de trading",
        null=True,
        blank=True,
    )  # TODO: Eliminar null y blank
    enabled = models.BooleanField(verbose_name="Habilitado")
    created_at = models.DateTimeField(
        auto_now_add=True, blank=True, verbose_name="Creado en"
    )
    updated_at = models.DateTimeField(
        auto_now=True, blank=True, verbose_name="Modificado en"
    )

    class Meta:
        verbose_name = "Porcentaje de ganancia por nivel de Trading"
        verbose_name_plural = "Porcentajes de ganancia por nivel de Trading"

    def __str__(self):
        return (
            f"{self.id} - {self.name} - Nivel {self.level} - {self.earnings_percentage}"
        )


class RootBarterUser(models.Model):
    user = models.ForeignKey(
        "barter_auth.BarterUser",
        on_delete=models.CASCADE,
        related_name="root_barter_user",
        verbose_name="Usuario raíz",
    )
    enabled = models.BooleanField(default=True, verbose_name="Habilitado")

    created_at = models.DateTimeField(
        auto_now_add=True, blank=True, verbose_name="Creado en"
    )
    updated_at = models.DateTimeField(
        auto_now=True, blank=True, verbose_name="Modificado en"
    )

    class Meta:
        verbose_name = "Usuario raíz de las redes"
        verbose_name_plural = "Usuarios raices de las redes"


class CapsByDirectUsers(models.Model):
    count_of_direct_users = models.PositiveSmallIntegerField(
        verbose_name="Cantidad de usuarios directos requeridos"
    )

    level_to_win = models.PositiveSmallIntegerField(
        verbose_name="Nivel que podrá generar ganancias"
    )

    enabled = models.BooleanField(default=True, verbose_name="Habilitado")

    created_at = models.DateTimeField(
        auto_now_add=True, blank=True, verbose_name="Creado en"
    )
    updated_at = models.DateTimeField(
        auto_now=True, blank=True, verbose_name="Modificado en"
    )

    class Meta:
        verbose_name = "Cantidad de usuarios directos para ganar"
        verbose_name_plural = "Cantidad de usuarios directos para ganar"

    def __str__(self):
        return f"Directos: {self.count_of_direct_users} - Nivel: {self.level_to_win}"
