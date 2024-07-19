from django.db.models import Sum
from rest_framework import serializers

from transactions.models import TransactionType, Transaction, Withdrawal, DetailCoFounderEarningByProducts, \
    CoFounderEarningByTrading, DetailCoFounderEarningByTrading, CoFounderEarningByProducts, ReInvestments

from drf_spectacular.utils import extend_schema_field
from drf_spectacular.types import OpenApiTypes


class TransactionTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionType
        fields = ['id', 'description']


class ListTransactionSerializer(serializers.ModelSerializer):
    # transaction_type = TransactionTypeSerializer(read_only=True)

    class Meta:
        model = Transaction
        fields = '__all__'


class WriteTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'


class WithdrawalSerializer(serializers.ModelSerializer):
    transaction_status_name = serializers.CharField(read_only=True)

    class Meta:
        model = Withdrawal
        fields = '__all__'
        # fields = '__all__'


class DetailCoFounderEarningByProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetailCoFounderEarningByProducts
        fields = '__all__'
        # fields = '__all__'


class DetailCoFounderEarningByTradingSerializer(serializers.ModelSerializer):
    year = serializers.SerializerMethodField()
    trimester = serializers.SerializerMethodField()
    month = serializers.SerializerMethodField()

    @extend_schema_field(OpenApiTypes.INT)
    def get_year(self, obj):
        return obj.co_founder_earning_by_trading.year

    @extend_schema_field(OpenApiTypes.INT)
    def get_trimester(self, obj):
        return obj.co_founder_earning_by_trading.trimester

    @extend_schema_field(OpenApiTypes.INT)
    def get_month(self, obj):
        return obj.co_founder_earning_by_trading.month

    class Meta:
        model = DetailCoFounderEarningByTrading
        fields = ['co_founder_earning_by_trading', 'month', 'year', 'trimester', 'earnings', 'earnings_paid']


class DetailCoFounderEarningByProductSerializer(serializers.ModelSerializer):
    year = serializers.SerializerMethodField()
    trimester = serializers.SerializerMethodField()
    month = serializers.SerializerMethodField()
    product = serializers.SerializerMethodField()
    product_name = serializers.SerializerMethodField()

    @extend_schema_field(OpenApiTypes.INT)
    def get_year(self, obj):
        return obj.co_founder_earning_by_products.year

    @extend_schema_field(OpenApiTypes.INT)
    def get_trimester(self, obj):
        return obj.co_founder_earning_by_products.trimester

    @extend_schema_field(OpenApiTypes.INT)
    def get_month(self, obj):
        return obj.co_founder_earning_by_products.month

    @extend_schema_field(OpenApiTypes.INT)
    def get_product(self, obj):
        return obj.co_founder_earning_by_products.product

    @extend_schema_field(OpenApiTypes.STR)
    def get_product_name(self, obj):
        return CoFounderEarningByProducts.PRODUCTS[obj.co_founder_earning_by_products.product][1]

    class Meta:
        model = DetailCoFounderEarningByProducts
        fields = ['co_founder_earning_by_products',
                  'month', 'year', 'trimester',
                  'earnings', 'earnings_paid', 'product', 'product_name']


class GeneralDetailCoFounderEarningByTradingSerializer(serializers.Serializer):
    total = serializers.SerializerMethodField()
    total_paid = serializers.SerializerMethodField()
    details = DetailCoFounderEarningByTradingSerializer(many=True)

    @extend_schema_field(field=OpenApiTypes.DECIMAL)
    def get_total(self, obj):
        return obj['total']

    @extend_schema_field(field=OpenApiTypes.DECIMAL)
    def get_total_paid(self, obj):
        return obj['total_paid']

    class Meta:
        fields = ('total', 'total_paid', 'details')


class GeneralDetailCoFounderEarningByProductsSerializer(serializers.Serializer):
    total = serializers.SerializerMethodField()
    total_paid = serializers.SerializerMethodField()
    details = DetailCoFounderEarningByProductSerializer(many=True)

    @extend_schema_field(field=OpenApiTypes.DECIMAL)
    def get_total(self, obj):
        return obj['total']
    
    @extend_schema_field(field=OpenApiTypes.DECIMAL)
    def get_total_paid(self, obj):
        return obj['total_paid']

    class Meta:
        fields = ('total', 'total_paid', 'details')


class ReInvestmentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReInvestments
        fields = '__all__'


class ReInvestmentsAvailableSerializer(serializers.Serializer):
    # string que significa plan de inversión
    plan = serializers.CharField()
    # capital actual del plan
    capital = serializers.DecimalField(max_digits=20, decimal_places=2)

    # ganancias del plan
    earnings = serializers.DecimalField(max_digits=20, decimal_places=2)

    # ganancias de red del plan
    network_earnings = serializers.DecimalField(max_digits=20, decimal_places=2)

    # total
    total = serializers.DecimalField(max_digits=20, decimal_places=2)
