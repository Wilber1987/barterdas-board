from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from barter_auth.models import (
    BarterUser,
    BarterPlan,
    BarterTradingPlan,
    BarterPlanCredentials,
    UserWallet,
    UnilevelNetwork,
)


# region Inlines
class BarterPlanCredentialInline(admin.TabularInline):
    model = BarterPlanCredentials
    extra = 0


class BarterPlanInline(admin.TabularInline):
    model = BarterPlan


class TradingPlanInline(admin.TabularInline):
    model = BarterTradingPlan
    extra = 0


class UnilevelNetworkUserInline(admin.TabularInline):
    model = UnilevelNetwork
    fk_name = "user"
    verbose_name = "Red"
    verbose_name_plural = "Red"

    readonly_fields = ["user", "user_in_network", "in_network_through", "level"]

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    can_delete = False


class UnilevelNetworkUserInNetworkInline(admin.TabularInline):
    model = UnilevelNetwork
    fk_name = "user_in_network"
    verbose_name = "Red presente"
    verbose_name = "Redes presente"

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    can_delete = False


# endregion


@admin.register(BarterUser)
class BarterUserAdmin(UserAdmin):
    search_fields = ("email", "username", "first_name", "last_name")
    list_display = (
        "id",
        "first_name",
        "last_name",
        "email",
        "is_active",
        "verified",
        "is_co_founder",
        "has_kyc",
        "has_network",
        "has_plan",
        "has_trading_plan",
    )
    list_filter = ["id", "email"]

    inlines = [
        UnilevelNetworkUserInline,
        UnilevelNetworkUserInNetworkInline,
        BarterPlanInline,
        TradingPlanInline,
    ]

    def has_kyc(self, obj):
        return obj.has_kyc

    def has_network(self, obj):
        return obj.has_network

    def has_plan(self, obj):
        return obj.has_plan

    def has_trading_plan(self, obj):
        return obj.has_trading_plan

    has_kyc.boolean = True
    has_kyc.short_description = "Tiene KYC"
    has_network.boolean = True
    has_network.short_description = "Tiene red"
    has_plan.boolean = True
    has_plan.short_description = "Tiene Kit Plan"
    has_trading_plan.boolean = True
    has_trading_plan.short_description = "Tiene Inversion Trading"

    # Override default UserAdmin sort for efficiency
    ordering = ["first_name", "last_name"]

    list_per_page = 30

    readonly_fields = [
        "referral_code",
        "last_login",
        "date_joined",
        "user_trading_balance_admin",
        "user_trading_earnings_balance_admin",
        "user_kitplan_balance_admin",
        "user_kitplan_network_earning_admin",
        "user_cofounder_balance_admin",
        "user_cofounder_balance_earnings_admin",
        "user_count_direct_users",
    ]

    # Create and edit field definitions
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (
            _("Personal info"),
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "email",
                    "country",
                    "zip_code",
                    "phone_number",
                    "profile_image",
                    "address",
                    "city",
                    "referral_code",
                    "referred_by",
                    "is_co_founder",
                    "verified",
                    "can_fill_kyc",
                    "leadership_pool_type",
                )
            },
        ),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
        (
            _("Balance"),
            {
                "fields": [
                    "user_trading_balance_admin",
                    "user_trading_earnings_balance_admin",
                    "user_kitplan_balance_admin",
                    "user_kitplan_network_earning_admin",
                    "user_cofounder_balance_admin",
                    "user_cofounder_balance_earnings_admin",
                    "user_count_direct_users",
                ]
            },
        ),
    )
    add_fieldsets = (
        (None, {"fields": ("username", "password1", "password2")}),
        (
            _("Personal info"),
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "email",
                    "country",
                    "zip_code",
                    "phone_number",
                    "profile_image",
                    "address",
                    "city",
                    "referral_code",
                    "is_co_founder",
                    "verified",
                )
            },
        ),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )

    # TODO: Add validations for current user group permissions
    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(UnilevelNetwork)
class UnilevelNetworkAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "level", "user_in_network", "in_network_through"]
    list_filter = ["user", "level", "user_in_network", "in_network_through"]
    ordering = ["user", "level"]
    list_per_page = 50

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(BarterPlanCredentials)
class BarterPlanCredentialsAdmin(admin.ModelAdmin):
    list_display = (
        "plan_user_name",
        "description",
        "kit_plan",
        "transaction_hash",
    )
    list_filter = ("plan__selected_plan",)
    search_fields = (
        "plan__user__first_name",
        "plan__user__last_name",
        "plan__transaction_hash",
    )
    ordering = ("plan__user",)
    list_per_page = 30

    @admin.display(ordering="plan__user", description="Usuario")
    def plan_user_name(self, obj):
        return obj.plan.user.get_full_name()

    @admin.display(description="Hash de transacción")
    def transaction_hash(self, obj):
        return f"{obj.plan.transaction_hash}"

    @admin.display(description="Kit Plan")
    def kit_plan(self, obj):
        return f"$ {obj.plan.selected_plan}"


@admin.register(UserWallet)
class UserWalletAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "hash", "blockchain", "exchange", "enabled"]
    search_fields = ["id", "user", "hash"]
    list_filter = ["user", "blockchain", "exchange"]

    list_per_page = 15

    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
