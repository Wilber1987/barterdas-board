from rest_framework import serializers

from barter_auth.models import BarterUser
from transactions.utils.user_balance_utils import get_user_current_cofounder_earnings, get_user_current_kitplan_earnings, get_user_current_trading_earnings
from transactions.models import Transaction, Withdrawal, KitPlanNetWorkEarnings, ReInvestments


class UserTransactionSerializer(serializers.ModelSerializer):
    "Serializer used for /user-transactions/ endpoint"

    class Meta:
        """Define serializer model and fields"""

        model = Transaction
        fields = [
            "wallet_address",
            "wallet_provider",
            "transaction_type",
            "transaction_network",
            "transaction_date",
            "transaction_hash",
            "amount",
            "voucher_screenshot",
            # * Read only fields
            "transaction_status",
            "description",
            "wallet_deposit_date",
        ]
        read_only_fields = ["transaction_status", "description", "wallet_deposit_date"]

class UserWithdrawalSerializer(serializers.ModelSerializer):
    """Serializer used for v2/user-withdrawals/ endpoint"""

    class Meta:
        """Define serializer model and fields"""

        model = Withdrawal
        fields = [
            "wallet_address",
            "wallet_provider",
            "other_wallet_provider",
            "wallet_network",
            "source_of_profit",
            "transaction_hash",
            "confirmation_screenshot",
            "transaction_status",
            "amount",
            "fee_amount",
            "amount_after_fee",
            "created_at",
            "transaction_date"
        ]
        read_only_fields = [
            "transaction_hash",
            "confirmation_screenshot",
            "transaction_status", 
            "fee_amount",
            "amount_after_fee",
            "created_at",
            "transaction_date"
        ]

    def validate_amount(self, value):
        if value < 10:
            raise serializers.ValidationError("The amount to be withdrawn must be greater than 10")
        
        return value
    
    def validate(self, attr):
        user:BarterUser = self.context.get('request').user
        sop = attr.get('source_of_profit')
        balance = 0

        if sop == 'TRADING':
            _,_,balance = get_user_current_trading_earnings(user)   # Get only total earning
        elif sop == 'KIT_PLAN':
            balance = get_user_current_kitplan_earnings(user)
        elif sop == 'CO_FOUNDER':
            _,_,balance = get_user_current_cofounder_earnings(user) # Get only total earning

        if float(attr.get("amount")) > balance:
            raise serializers.ValidationError("The amount to be withdrawn must be less than or equal to the user's current earnings") 

        return attr


class UserReinvestmentsSerializer(serializers.ModelSerializer):
    """Serializer used for v2/user-reinvestment/ endpoint"""
    class Meta:
        model = ReInvestments
        fields = (
            "amount",
            "type_re_investment",
            "created_at",
        )
        read_only_fields = (
            "created_at",
        )

    def validate_amount(self, value):
        if value < 10:
            raise serializers.ValidationError("The amount to be reinvested must be greater than 10")

        return value
    
    def validate(self, attr):
        user:BarterUser = self.context.get('request').user
        sop = attr.get('type_re_investment')
        balance = 0

        if sop == 'Trading':
            _,_,balance = get_user_current_trading_earnings(user)   # Get only total earning
        elif sop == 'Co-Founder':
            _,_,balance = get_user_current_cofounder_earnings(user) # Get only total earning

        if float(attr.get("amount")) > balance:
            raise serializers.ValidationError("The amount to be reinvested must be less than or equal to the user's current earnings") 

        return super().validate(attr)


class UserEarningsGraphicDetailSerializer(serializers.Serializer):
    month = serializers.IntegerField()
    label = serializers.CharField()
    value = serializers.DecimalField(max_digits=10, decimal_places=2)

class UserEarningsGraphicTypeSerializer(serializers.Serializer):
    id = serializers.CharField()
    label = serializers.CharField()
    data = UserEarningsGraphicDetailSerializer(many=True)
    
class UserEarningGraphicSerializer(serializers.Serializer):
    year = serializers.IntegerField()
    earnings = UserEarningsGraphicTypeSerializer(many=True)


class WithdrawalSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.HyperlinkedRelatedField(
        many=False,
        read_only=False,
        queryset=BarterUser.objects.all(),
        view_name='barteruser-detail'
    )

    class Meta:
        model = Withdrawal
        fields = (
            'url',
            'pk',
            'user',
            'wallet_address',
            'wallet_provider',
            'other_wallet_provider',
            'wallet_network',
            'source_of_profit',
            'transaction_hash',
            'voucher_screenshot',
            'confirmation_screenshot',
            'amount',
            'transaction_status',
            'fee_amount',
            'amount_after_fee',
            'created_at',
            'transaction_date',
        )


class KitPlanEarningsSerializer(serializers.ModelSerializer):
    class Meta:
        model = KitPlanNetWorkEarnings
        fields = (
            'pk',
            'level',
            'level_earnings_percentage',
            'earnings',
        )