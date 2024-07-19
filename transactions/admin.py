from django.contrib import admin
from django.utils.html import format_html

from transactions.models import *


# Inline for transaction screenshots
class TransactionScreenshotInline(admin.TabularInline):
    model = TransactionScreenshot
    extra = 0


# Inline for balance history
class BalanceInline(admin.StackedInline):
    model = Balance
    extra = 0

    verbose_name = 'Balance'
    verbose_name_plural = 'Balance'

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False

    can_delete = False


# Register your models here.
@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    search_fields = ('transaction_hash', 'user__first_name', 'user__last_name')
    list_display = (
        'id', 'user', 'transaction_type', 'amount', 'transaction_date', 'wallet_deposit_date', 'transaction_hash',
        'img_voucher', 'transaction_status', 'calculated_earnings')
    list_filter = ('user', 'transaction_type', 'transaction_date', 'transaction_status')
    ordering = ('user',)
    list_per_page = 30
    inlines = [TransactionScreenshotInline, ]

    @admin.display(description='Captura Voucher', empty_value='No hay imagen')
    def img_voucher(self, obj):
        return format_html(
            f'<a href="{obj.voucher_screenshot}"><img src="{obj.voucher_screenshot}" style="max-height: 30px;"/></a>')

@admin.register(Withdrawal)
class WithdrawalAdmin(admin.ModelAdmin):
    search_fields = ('transaction_hash', 'user__first_name', 'user__last_name')
    list_display = ('id', 'user', 'amount', 'transaction_status', 'source_of_profit', 'created_at')
    list_filter = ('transaction_status', 'source_of_profit')
    list_per_page = 30


@admin.register(MonthlyTradingEarnings)
class MonthlyTradingEarningsAdmin(admin.ModelAdmin):
    list_display = ['id', 'roi', 'month', 'year', 'created_at']
    list_filter = ('month', 'year',)
    ordering = ('created_at',)


@admin.register(CoFounderEarningByProducts)
class CoFounderEarningByProductsAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'leadership_pool_type', 'earning_percentage', 'trimester', 'month', 'year',
                    'created_at']
    list_filter = ('product', 'month', 'trimester', 'year', 'earning_percentage', 'leadership_pool_type')
    ordering = ('created_at', 'leadership_pool_type')
    readonly_fields = ['trimester']


@admin.register(CoFounderEarningByTrading)
class CoFounderEarningByProductsAdmin(admin.ModelAdmin):
    list_display = ['id', 'earning_percentage', 'leadership_pool_type', 'month', 'year', 'created_at']
    list_filter = ('month', 'trimester', 'leadership_pool_type', 'year', 'earning_percentage')
    ordering = ('created_at', 'leadership_pool_type')
    readonly_fields = ['trimester']


@admin.register(DetailCoFounderEarningByProducts)
class DetailCoFounderEarningByProductsAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'co_founder_earning_by_products', 'earnings', 'earnings_paid', 'created_at']
    list_filter = ('co_founder_earning_by_products__month', 'co_founder_earning_by_products__trimester',
                   'co_founder_earning_by_products__year', 'co_founder_earning_by_products__earning_percentage')

    ordering = ('created_at',)
    search_fields = (
        'user__first_name', 'user__last_name', 'co_founder_earning_by_products__month',
        'co_founder_earning_by_products__year')


@admin.register(DetailCoFounderEarningByTrading)
class DetailCoFounderEarningByTradingAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'co_founder_earning_by_trading', 'earnings', 'earnings_paid', 'created_at']
    list_filter = ('co_founder_earning_by_trading__month', 'co_founder_earning_by_trading__trimester',
                   'co_founder_earning_by_trading__year', 'co_founder_earning_by_trading__earning_percentage')
    ordering = ('created_at',)
    search_fields = (
        'user__first_name', 'user__last_name', 'co_founder_earning_by_trading__month',
        'co_founder_earning_by_trading__year')


@admin.register(ReInvestments)
class ReInvestmentsAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'amount', 'type_re_investment', 'created_at']
    list_filter = ('created_at', 'type_re_investment', 'user')
    ordering = ('created_at',)
    search_fields = (
        'user__first_name', 'user__last_name', 'type_re_investment', 'created_at')


@admin.register(BalanceHistory)
class BalanceHistoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'balance', 'balance_transaction_type', 'object_id', 'object_date', 'amount', 'enabled']
    list_filter = ('created_at', 'enabled', 'balance_transaction_type__name', 'object_date')
    ordering = ('balance__id',)
    search_fields = ('balance__user__first_name', 'balance__user__last_name', 'object_id')

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(BalanceTransactionType)
class BalanceTradingTypeAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'unique_code',
        'description',
        'app_lookup',
        'model_lookup',
        'balance_lookup_field',
        'is_income',
        'enabled'
    )

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(KitPlanNetWorkEarnings)
class KitPlanNetWorkEarningsAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_network', 'user_in_network', 'transaction',
                    'level','level_earnings_percentage', 'current_investment', 'earnings', 'created_at']
    list_filter = ('created_at', 'level', 'unilevel_network__user', 'unilevel_network__user_in_network')
    ordering = ('created_at',)


@admin.register(TradingNetWorkEarnings)
class TradingNetWorkEarningsAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_network', 'user_in_network', 'trading_earnings_id',
                    'level', 'current_investment', 'level_earnings_percentage', 'earnings', 'created_at']
    list_filter = (
        'created_at', 'level', 'unilevel_network__user', 'unilevel_network__user_in_network', 'trading_percentage')
    ordering = ('created_at',)



@admin.register(TradingEarnings)
class TradingEarningsAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'type_earning', 'trading_percentage_used', 'current_investment', 'earnings',
                    'calculated_earnings']
    list_filter = ('created_at', 'user', 'trading_percentage', 'transaction', 'reinvestment')
    ordering = ('created_at',)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "reinvestment":
            kwargs["queryset"] = ReInvestments.objects.filter(type_re_investment=ReInvestments.TYPE_RE_INVESTMENT[0][0])
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
