from django.contrib import admin
from global_settings.models import WithdrawalType, KitPlan, KitPlanDetail, BusinessWallet, \
    BlockchainChoices, ExchangeChoices, LeadershipPoolType, \
    KitPlanUnilevelPercentage, TradingUnilevelPercentage, \
    BusinessWalletType, RootBarterUser, CryptocurrencyChoices, \
    KitPlanCategory, TradingPlans, CapsByDirectUsers


# Operations Mixins
class DisableDeleteOperation:
    def has_delete_permission(self, request, obj=None):
        return False


class DisableUpdateOperation:
    def has_change_permission(self, request, obj=None):
        return False


# Inlines
class KitPlanDetailInline(admin.TabularInline):
    model = KitPlanDetail
    extra = 0


# Admin Models
@admin.register(WithdrawalType)
class WithdrawalTypeAdmin(DisableDeleteOperation, admin.ModelAdmin):
    list_display = ('id', 'description', 'value', 'enabled')


@admin.register(KitPlanCategory)
class KitPlanCategoryAdmin(DisableDeleteOperation, admin.ModelAdmin):
    list_display = ['id', 'name', 'enabled']
    search_fields = ['name']
    ordering = ['name']
    list_per_page = 30


@admin.register(KitPlan)
class KitPlanAdmin(DisableDeleteOperation, admin.ModelAdmin):
    list_display = ['id', 'title', 'price', 'enabled']
    search_fields = ['id', 'title']
    list_filter = ['enabled', 'price']
    readonly_fields = ['created_at', 'updated_at']
    list_per_page = 15

    inlines = [KitPlanDetailInline]


@admin.register(TradingPlans)
class TradingPlanAdmin(admin.ModelAdmin):
    list_display = ['id', 'code', 'name', 'price', 'cap', 'enabled']
    search_fields = ['id', 'code']
    list_filter = ['enabled', 'price']
    readonly_fields = ['created_at', 'updated_at']
    list_per_page = 15


@admin.register(BusinessWalletType)
class BusinessWalletTypeAdmin(DisableDeleteOperation, admin.ModelAdmin):
    list_display = ['id', 'name', 'enabled']
    search_fields = ['name']
    ordering = ['name']
    list_per_page = 30


@admin.register(BusinessWallet)
class BusinessWalletAdmin(DisableDeleteOperation, admin.ModelAdmin):
    list_display = ['id', 'hash', 'blockchain', 'exchange', 'enabled']
    search_fields = ['id', 'hash']
    list_filter = ['enabled']
    list_editable = ['enabled']

    list_per_page = 15


@admin.register(ExchangeChoices)
class ExchangeChoicesAdmin(DisableDeleteOperation, admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']

    list_per_page = 15


@admin.register(BlockchainChoices)
class BlockchainChoicesAdmin(DisableDeleteOperation, admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']

    list_per_page = 15


@admin.register(CryptocurrencyChoices)
class CryptocurrencyChoicesAdmin(DisableDeleteOperation, admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']

    list_per_page = 15


@admin.register(LeadershipPoolType)
class LeadershipPoolTypeAdmin(DisableDeleteOperation, admin.ModelAdmin):
    list_display = ['id', 'name', 'earning_percentage', 'enabled']
    search_fields = ['name']
    list_filter = ['id', 'earning_percentage', 'enabled']


@admin.register(KitPlanUnilevelPercentage)
class KitPlanUnilevelPercentageAdmin(DisableDeleteOperation, admin.ModelAdmin):
    list_display = ['id', 'name', 'kit_plan', 'level', 'earnings_percentage', 'enabled']
    search_fields = ['id', 'name']
    list_editable = ['name', 'kit_plan', 'level', 'earnings_percentage', 'enabled']
    list_filter = ['id', 'level', 'kit_plan']
    list_per_page = 15

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "kit_plan":
            kwargs["queryset"] = KitPlan.objects.filter(enabled=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(TradingUnilevelPercentage)
class TradingUnilevelPercentageAdmin(DisableDeleteOperation, admin.ModelAdmin):
    list_display = ['id', 'name', 'trading_plan', 'level', 'earnings_percentage', 'enabled']
    search_fields = ['id', 'name']
    list_editable = ['name', 'trading_plan', 'level', 'earnings_percentage', 'enabled']
    list_filter = ['trading_plan', 'level']
    list_per_page = 15


@admin.register(RootBarterUser)
class RootBarterUserAdmin(admin.ModelAdmin):
    list_display = ['user', 'enabled', 'created_at', 'updated_at']
    search_fields = ['user__username', 'user__first_name', 'user__last_name']
    list_filter = ['enabled']


@admin.register(CapsByDirectUsers)
class CapsByDirectUsersAdmin(admin.ModelAdmin):
    list_display = ['id', 'count_of_direct_users', 'level_to_win', 'enabled']
    search_fields = ['id', 'count_of_direct_users']
    list_filter = ['enabled']
    list_per_page = 15