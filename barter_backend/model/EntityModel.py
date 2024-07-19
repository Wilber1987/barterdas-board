# Clases generadas din�micamente
from barter_backend.core.EntityClass import EntityClass
import datetime

class Django_migrations(EntityClass):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.id: int = None
        self.applied: str = None
        self.app: str = None
        self.name: str = None
        for key, value in kwargs.items():
            setattr(self, key, value)

class Django_content_type(EntityClass):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.id: int = None
        self.app_label: str = None
        self.model: str = None
        for key, value in kwargs.items():
            setattr(self, key, value)

class Auth_permission(EntityClass):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.id: int = None
        self.content_type_id: int = None
        self.name: str = None
        self.codename: str = None
        for key, value in kwargs.items():
            setattr(self, key, value)

class Auth_group(EntityClass):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.id: int = None
        self.name: str = None
        for key, value in kwargs.items():
            setattr(self, key, value)

class Auth_group_permissions(EntityClass):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.id: int = None
        self.group_id: int = None
        self.permission_id: int = None
        for key, value in kwargs.items():
            setattr(self, key, value)

class Barter_auth_barteruser_groups(EntityClass):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.id: int = None
        self.barteruser_id: int = None
        self.group_id: int = None
        for key, value in kwargs.items():
            setattr(self, key, value)

class Barter_auth_referral(EntityClass):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.id: int = None
        self.amount: str = None
        self.investment_id: int = None
        self.user_id: int = None
        self.transaction_hash: str = None
        self.category: str = None
        for key, value in kwargs.items():
            setattr(self, key, value)

class Barter_auth_barterusersecurityprofile(EntityClass):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.id: int = None
        self.terms_and_conditions: bool = None
        self.user_id: int = None
        self.dni_image: str = None
        self.dni_back_image: str = None
        for key, value in kwargs.items():
            setattr(self, key, value)

class Barter_auth_barteruser_user_permissions(EntityClass):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.id: int = None
        self.barteruser_id: int = None
        self.permission_id: int = None
        for key, value in kwargs.items():
            setattr(self, key, value)

class Knox_authtoken(EntityClass):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.created: str = None
        self.user_id: int = None
        self.expiry: str = None
        self.digest: str = None
        self.token_key: str = None
        for key, value in kwargs.items():
            setattr(self, key, value)

class Django_admin_log(EntityClass):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.user_id: int = None
        self.action_time: str = None
        self.action_flag: str = None
        self.content_type_id: int = None
        self.id: int = None
        self.object_id: str = None
        self.object_repr: str = None
        self.change_message: str = None
        for key, value in kwargs.items():
            setattr(self, key, value)

class Barter_auth_barterusernode(EntityClass):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.id: int = None
        self.investment_id: int = None
        self.user_id: int = None
        self.node_level: int = None
        self.category: str = None
        self.reference_code: str = None
        for key, value in kwargs.items():
            setattr(self, key, value)

class Barter_auth_verificationactions(EntityClass):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.id: int = None
        self.token: str = None
        self.used: bool = None
        self.type: int = None
        self.expiration_date: str = None
        self.user_id: int = None
        for key, value in kwargs.items():
            setattr(self, key, value)

class Django_session(EntityClass):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.expire_date: str = None
        self.session_key: str = None
        self.session_data: str = None
        for key, value in kwargs.items():
            setattr(self, key, value)

class Django_site(EntityClass):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.id: int = None
        self.domain: str = None
        self.name: str = None
        for key, value in kwargs.items():
            setattr(self, key, value)

class Global_settings_kitplandetail(EntityClass):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.id: int = None
        self.position: str = None
        self.created_at: str = None
        self.updated_at: str = None
        self.kit_plan_id: int = None
        self.description: str = None
        for key, value in kwargs.items():
            setattr(self, key, value)

class Transactions_transactiontype(EntityClass):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.id: int = None
        self.description: str = None
        for key, value in kwargs.items():
            setattr(self, key, value)

class Global_settings_withdrawaltype(EntityClass):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.id: int = None
        self.value: str = None
        self.enabled: bool = None
        self.description: str = None
        for key, value in kwargs.items():
            setattr(self, key, value)

class Transactions_transaction(EntityClass):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.id: int = None
        self.amount: str = None
        self.created_at: str = None
        self.user_id: int = None
        self.transaction_status: int = None
        self.co_founder_invest: bool = None
        self.transaction_date: str = None
        self.updated_on: str = None
        self.wallet_deposit_date: str = None
        self.calculated_earnings: bool = None
        self.wallet_provider: str = None
        self.description: str = None
        self.transaction_hash: str = None
        self.transaction_type: str = None
        self.transaction_network: str = None
        self.voucher_screenshot: str = None
        self.wallet_address: str = None
        for key, value in kwargs.items():
            setattr(self, key, value)

class Global_settings_kitplan(EntityClass):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.kit_plan_category_id: int = None
        self.updated_at: str = None
        self.id: int = None
        self.price: str = None
        self.business_volume: str = None
        self.earnings_cap: str = None
        self.allow_repurchase: bool = None
        self.can_be_upgraded: bool = None
        self.enabled: bool = None
        self.created_at: str = None
        self.title: str = None
        self.short_description: str = None
        for key, value in kwargs.items():
            setattr(self, key, value)

class Barter_auth_barterplan(EntityClass):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.transaction_id: int = None
        self.selected_plan: str = None
        self.id: int = None
        self.user_id: int = None
        self.created_at: str = None
        self.cap_reached: bool = None
        self.plan_id: int = None
        self.transaction_hash: str = None
        for key, value in kwargs.items():
            setattr(self, key, value)

class Barter_auth_barterplancredentials(EntityClass):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.start_date: datetime = None
        self.plan_id: int = None
        self.end_date: datetime = None
        self.id: int = None
        self.created_at: str = None
        self.username: str = None
        self.password: str = None
        self.description: str = None
        for key, value in kwargs.items():
            setattr(self, key, value)

class Transactions_transactionscreenshot(EntityClass):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.id: int = None
        self.transaction_date: datetime = None
        self.created_at: str = None
        self.transaction_id: int = None
        self.voucher_screenshot: str = None
        for key, value in kwargs.items():
            setattr(self, key, value)

class Transactions_monthlytradingearnings(EntityClass):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.id: int = None
        self.roi: str = None
        self.month: int = None
        self.year: int = None
        self.created_at: str = None
        for key, value in kwargs.items():
            setattr(self, key, value)

class Sales_funnel_funnelstep(EntityClass):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.id: int = None
        self.step_number: str = None
        self.created_at: str = None
        self.updated_at: str = None
        self.next_step_id: int = None
        self.enabled: bool = None
        self.title: str = None
        self.youtube_video_url: str = None
        self.thumbnail_image: str = None
        for key, value in kwargs.items():
            setattr(self, key, value)

class Sales_funnel_salesfunnelowner(EntityClass):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.id: int = None
        self.enabled: bool = None
        self.created_at: str = None
        self.updated_at: str = None
        self.user_id: int = None
        self.facebook_account_url: str = None
        self.twitter_account_url: str = None
        self.custom_video_url: str = None
        self.profile_image: str = None
        self.username: str = None
        self.display_name: str = None
        self.email: str = None
        self.whatsapp_phone_number: str = None
        for key, value in kwargs.items():
            setattr(self, key, value)

class Sales_funnel_newslettersubscription(EntityClass):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.enabled: bool = None
        self.subscribed_to_id: int = None
        self.sent_emails: str = None
        self.id: int = None
        self.created_at: str = None
        self.updated_at: str = None
        self.subscriptor_email: str = None
        for key, value in kwargs.items():
            setattr(self, key, value)

class Transactions_monthlytradingearningsperleader(EntityClass):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.earnings_paid: str = None
        self.earnings: str = None
        self.id: int = None
        self.status: int = None
        self.created_at: str = None
        self.monthly_trading_earnings_id: int = None
        self.user_id: int = None
        self.calculation_process: str = None
        for key, value in kwargs.items():
            setattr(self, key, value)

class Transactions_cumulativerevenue(EntityClass):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.id: int = None
        self.total_earnings: str = None
        self.total_to_withdraw: str = None
        self.month: int = None
        self.year: int = None
        self.created_at: str = None
        self.user_id: int = None
        for key, value in kwargs.items():
            setattr(self, key, value)

class Transactions_withdrawal(EntityClass):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        #self.withdrawal_type_id: int = None
        self.amount: str = None
        self.transaction_status: int = None
        self.created_at: str = None
        self.user_id: int = None
        self.transaction_date: str = None
        self.fee_amount: str = None
        self.amount_after_fee: str = None
        self.id: int = None
        self.wallet_address: str = None
        self.wallet_provider: str = None
        self.wallet_network: str = None
        self.transaction_hash: str = None
        self.voucher_screenshot: str = None
        self.confirmation_screenshot: str = None
        self.other_wallet_provider: str = None
        self.source_of_profit: str = None
        for key, value in kwargs.items():
            setattr(self, key, value)

class Barter_auth_bartertradingplan(EntityClass):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.transaction_id: int = None
        self.trading_amount: str = None
        self.id: int = None
        self.user_id: int = None
        self.created_at: str = None
        self.cap_reached: bool = None
        self.plan_id: int = None
        self.transaction_hash: str = None
        for key, value in kwargs.items():
            setattr(self, key, value)

class Kyc_verifications_kycverificationresult(EntityClass):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.created_at_ms: str = None
        self.json_data: str = None
        self.id: int = None
        self.correlation_id: str = None
        self.level_name: str = None
        self.type: str = None
        self.review_status: str = None
        self.external_user_id: str = None
        self.applicant_id: str = None
        self.inspection_id: str = None
        for key, value in kwargs.items():
            setattr(self, key, value)

class Kyc_verifications_kycreviewresult(EntityClass):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.id: int = None
        self.verification_result_id: int = None
        self.client_comment: str = None
        self.reject_labels: str = None
        self.review_reject_type: str = None
        self.review_answer: str = None
        self.moderation_comment: str = None
        for key, value in kwargs.items():
            setattr(self, key, value)

class Global_settings_blockchainchoices(EntityClass):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.id: int = None
        self.name: str = None
        for key, value in kwargs.items():
            setattr(self, key, value)

class Global_settings_exchangechoices(EntityClass):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.id: int = None
        self.name: str = None
        for key, value in kwargs.items():
            setattr(self, key, value)

class Barter_auth_userwallet(EntityClass):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.id: int = None
        self.enabled: bool = None
        self.blockchain_id: int = None
        self.exchange_id: int = None
        self.user_id: int = None
        self.hash: str = None
        for key, value in kwargs.items():
            setattr(self, key, value)

class Transactions_userdailytradingrevenue(EntityClass):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.id: int = None
        self.current_investment: str = None
        self.earnings_percentage: str = None
        self.earnings: str = None
        self.earnings_date: datetime = None
        self.enabled: bool = None
        self.created_at: str = None
        self.updated_at: str = None
        self.daily_percentage_revenue_id: int = None
        self.transaction_id: int = None
        self.user_id: int = None
        self.cumulative_revenue_id: int = None
        self.reinvestment_id: int = None
        self.calculated_earnings: bool = None
        for key, value in kwargs.items():
            setattr(self, key, value)

class Transactions_cofounderearningbyproducts(EntityClass):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.id: int = None
        self.earning_percentage: str = None
        self.product: int = None
        self.month: int = None
        self.trimester: int = None
        self.year: int = None
        self.created_at: str = None
        self.leadership_pool_type_id: int = None
        for key, value in kwargs.items():
            setattr(self, key, value)

class Global_settings_businesswallet(EntityClass):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cryptocurrency_id: int = None
        self.type_id: int = None
        self.id: int = None
        self.enabled: bool = None
        self.blockchain_id: int = None
        self.exchange_id: int = None
        self.hash: str = None
        self.qr_code: str = None
        for key, value in kwargs.items():
            setattr(self, key, value)

class Transactions_dailypercentagerevenue(EntityClass):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.id: int = None
        self.date: datetime = None
        self.percentage_amount: str = None
        self.created_at: str = None
        self.enabled: bool = None
        self.updated_at: str = None
        for key, value in kwargs.items():
            setattr(self, key, value)

class Transactions_detailcofounderearningbyproducts(EntityClass):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.id: int = None
        self.earnings: str = None
        self.earnings_paid: str = None
        self.created_at: str = None
        self.co_founder_earning_by_products_id: int = None
        self.user_id: int = None
        self.process: str = None
        for key, value in kwargs.items():
            setattr(self, key, value)

class Transactions_detailcofounderearningbytrading(EntityClass):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.id: int = None
        self.earnings: str = None
        self.earnings_paid: str = None
        self.created_at: str = None
        self.co_founder_earning_by_trading_id: int = None
        self.user_id: int = None
        self.process: str = None
        for key, value in kwargs.items():
            setattr(self, key, value)

class Transactions_balance(EntityClass):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.id: int = None
        self.cofounder_balance: str = None
        self.cofounder_earnings: str = None
        self.trading_balance: str = None
        self.trading_earnings: str = None
        self.trading_network_earnings: str = None
        self.kitplan_balance: str = None
        self.kitplan_network_earnings: str = None
        self.enabled: bool = None
        self.created_at: str = None
        self.updated_at: str = None
        self.user_id: int = None
        self.general_balance: str = None
        for key, value in kwargs.items():
            setattr(self, key, value)

class Global_settings_leadershippooltype(EntityClass):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.earning_percentage: str = None
        self.created_at: str = None
        self.updated_at: str = None
        self.id: int = None
        self.enabled: bool = None
        self.name: str = None
        self.description: str = None
        for key, value in kwargs.items():
            setattr(self, key, value)

class Transactions_reinvestments(EntityClass):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.id: int = None
        self.amount: str = None
        self.created_at: str = None
        self.user_id: int = None
        self.type_re_investment: str = None
        for key, value in kwargs.items():
            setattr(self, key, value)

class Email_app_funnelpurchasesentemail(EntityClass):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.id: int = None
        self.sent_at: str = None
        self.transaction_id: int = None
        self.user_id: int = None
        for key, value in kwargs.items():
            setattr(self, key, value)

class Transactions_cofounderearningbytrading(EntityClass):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.id: int = None
        self.earning_percentage: str = None
        self.month: int = None
        self.trimester: int = None
        self.year: int = None
        self.created_at: str = None
        self.leadership_pool_type_id: int = None
        for key, value in kwargs.items():
            setattr(self, key, value)

class Global_settings_kitplanunilevelpercentage(EntityClass):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.kit_plan_id: int = None
        self.updated_at: str = None
        self.id: int = None
        self.level: str = None
        self.earnings_percentage: str = None
        self.enabled: bool = None
        self.created_at: str = None
        self.name: str = None
        self.description: str = None
        for key, value in kwargs.items():
            setattr(self, key, value)

class Transactions_balancehistory(EntityClass):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.id: int = None
        self.object_id: int = None
        self.object_date: str = None
        self.amount: str = None
        self.enabled: bool = None
        self.created_at: str = None
        self.updated_at: str = None
        self.balance_id: int = None
        self.balance_transaction_type_id: int = None
        for key, value in kwargs.items():
            setattr(self, key, value)

class Global_settings_tradingunilevelpercentage(EntityClass):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.trading_plan_id: int = None
        self.updated_at: str = None
        self.id: int = None
        self.level: str = None
        self.earnings_percentage: str = None
        self.enabled: bool = None
        self.created_at: str = None
        self.name: str = None
        self.description: str = None
        for key, value in kwargs.items():
            setattr(self, key, value)

class Transactions_dailytradingrevenue(EntityClass):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.id: int = None
        self.current_investment: str = None
        self.earnings_percentage: str = None
        self.earnings: str = None
        self.earnings_date: datetime = None
        self.enabled: bool = None
        self.created_at: str = None
        self.updated_at: str = None
        self.balance_history_checkpoint_id: int = None
        self.daily_percentage_revenue_id: int = None
        self.user_id: int = None
        for key, value in kwargs.items():
            setattr(self, key, value)

class Transactions_balancetransactiontype(EntityClass):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.is_income: bool = None
        self.enabled: bool = None
        self.created_at: str = None
        self.updated_at: str = None
        self.id: int = None
        self.balance_lookup_field: str = None
        self.unique_code: str = None
        self.name: str = None
        self.description: str = None
        self.app_lookup: str = None
        self.model_lookup: str = None
        for key, value in kwargs.items():
            setattr(self, key, value)

class Transactions_cofoundermonthlyearningtype(EntityClass):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.enabled: bool = None
        self.created_at: str = None
        self.updated_at: str = None
        self.id: int = None
        self.description: str = None
        self.name: str = None
        self.unique_code: str = None
        for key, value in kwargs.items():
            setattr(self, key, value)

class Transactions_cofoundermonthlyearning(EntityClass):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.id: int = None
        self.earning_percentage: str = None
        self.month: str = None
        self.year: str = None
        self.trimester: str = None
        self.enabled: bool = None
        self.created_at: str = None
        self.updated_at: str = None
        self.cofounder_monthly_earning_type_id: int = None
        self.leadership_pool_type_id: int = None
        for key, value in kwargs.items():
            setattr(self, key, value)

class Transactions_cofoundermonthlyearningdetail(EntityClass):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.id: int = None
        self.current_investment: str = None
        self.cofounder_monthly_earning_percentage: str = None
        self.wallet_deposit_date: str = None
        self.earnings: str = None
        self.enabled: bool = None
        self.created_at: str = None
        self.updated_at: str = None
        self.balance_history_id: int = None
        self.cofounder_monthly_earning_id: int = None
        self.user_id: int = None
        self.wallet_deposit_multiplier: str = None
        for key, value in kwargs.items():
            setattr(self, key, value)

class Transactions_tradinglevelpercentage(EntityClass):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.level: int = None
        self.updated_at: str = None
        self.id: int = None
        self.percentage: str = None
        self.enabled: bool = None
        self.created_at: str = None
        self.name: str = None
        self.description: str = None
        for key, value in kwargs.items():
            setattr(self, key, value)

class Transactions_kitplanlevelpercentage(EntityClass):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.level: int = None
        self.updated_at: str = None
        self.id: int = None
        self.percentage: str = None
        self.enabled: bool = None
        self.created_at: str = None
        self.name: str = None
        self.description: str = None
        for key, value in kwargs.items():
            setattr(self, key, value)

class Transactions_tradingnetworkearnings(EntityClass):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.unilevel_network_id: int = None
        self.level: int = None
        self.level_earnings_percentage: str = None
        self.current_investment: str = None
        self.earnings: str = None
        self.id: int = None
        self.enabled: bool = None
        self.created_at: str = None
        self.updated_at: str = None
        self.trading_earnings_id: int = None
        self.trading_percentage_id: int = None
        self.trading_unilevel_network_id: int = None
        self.calculation_process: str = None
        for key, value in kwargs.items():
            setattr(self, key, value)

class Transactions_tradingearnings(EntityClass):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.reinvestment_id: int = None
        self.trading_percentage_used: str = None
        self.current_investment: str = None
        self.earnings: str = None
        self.id: int = None
        self.calculated_earnings: bool = None
        self.enabled: bool = None
        self.created_at: str = None
        self.updated_at: str = None
        self.trading_percentage_id: int = None
        self.transaction_id: int = None
        self.user_id: int = None
        self.calculation_process: str = None
        for key, value in kwargs.items():
            setattr(self, key, value)

class Kyc_verifications_kycmanualverificationdetail(EntityClass):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.id: int = None
        self.external_user_id_id: int = None
        self.applicant_id: str = None
        self.level_name: str = None
        self.review_status: str = None
        self.review_answer: str = None
        for key, value in kwargs.items():
            setattr(self, key, value)

class Barter_auth_unilevelnetwork(EntityClass):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.id: int = None
        self.level: int = None
        self.in_network_through_id: int = None
        self.user_id: int = None
        self.user_in_network_id: int = None
        for key, value in kwargs.items():
            setattr(self, key, value)

class Barter_auth_plansearnings(EntityClass):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.id: int = None
        self.earning: str = None
        self.status: int = None
        self.created_at: str = None
        self.user_id: int = None
        self.earning_paid: str = None
        self.month: int = None
        self.year: int = None
        for key, value in kwargs.items():
            setattr(self, key, value)

class Barter_auth_plansearningsdetail(EntityClass):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.created_at: str = None
        self.earning: str = None
        self.level: int = None
        self.id: int = None
        self.plan_earning_id: int = None
        self.transaction_id: int = None
        self.calculation_process: str = None
        for key, value in kwargs.items():
            setattr(self, key, value)

class Transactions_kitplannetworkearnings(EntityClass):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.unilevel_network_id: int = None
        self.level: int = None
        self.level_earnings_percentage: str = None
        self.current_investment: str = None
        self.earnings: str = None
        self.id: int = None
        self.enabled: bool = None
        self.created_at: str = None
        self.updated_at: str = None
        self.kit_plan_unilevel_network_id: int = None
        self.transaction_id: int = None
        self.calculation_process: str = None
        for key, value in kwargs.items():
            setattr(self, key, value)

class Global_settings_rootbarteruser(EntityClass):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.id: int = None
        self.enabled: bool = None
        self.created_at: str = None
        self.updated_at: str = None
        self.user_id: int = None
        for key, value in kwargs.items():
            setattr(self, key, value)

class Global_settings_businesswallettype(EntityClass):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.id: int = None
        self.enabled: bool = None
        self.created_at: str = None
        self.updated_at: str = None
        self.name: str = None
        self.description: str = None
        for key, value in kwargs.items():
            setattr(self, key, value)

class Global_settings_tradingplans(EntityClass):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.updated_at: str = None
        self.enabled: bool = None
        self.created_at: str = None
        self.id: int = None
        self.price: str = None
        self.cap: str = None
        self.code: str = None
        self.name: str = None
        self.description: str = None
        for key, value in kwargs.items():
            setattr(self, key, value)

class Global_settings_cryptocurrencychoices(EntityClass):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.id: int = None
        self.name: str = None
        for key, value in kwargs.items():
            setattr(self, key, value)

class Global_settings_kitplancategory(EntityClass):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.id: int = None
        self.enabled: bool = None
        self.created_at: str = None
        self.updated_at: str = None
        self.name: str = None
        self.description: str = None
        for key, value in kwargs.items():
            setattr(self, key, value)

class Global_settings_capsbydirectusers(EntityClass):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.id: int = None
        self.count_of_direct_users: str = None
        self.level_to_win: str = None
        self.enabled: bool = None
        self.created_at: str = None
        self.updated_at: str = None
        for key, value in kwargs.items():
            setattr(self, key, value)

