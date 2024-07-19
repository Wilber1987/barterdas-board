from rest_framework import serializers
from global_settings.models import (
    WithdrawalType,
    KitPlan,
    BlockchainChoices,
    ExchangeChoices,
    BusinessWallet,
)


class WithdrawalTypeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = WithdrawalType
        fields = (
            # 'url',
            "id",
            "description",
            "value",
            "enabled",
        )


class KitPlanSerializer(serializers.HyperlinkedModelSerializer):
    details = serializers.SerializerMethodField()

    kit_plan_category = serializers.SlugRelatedField(read_only=True, slug_field="name")

    class Meta:
        model = KitPlan
        fields = (
            # 'url',
            "pk",
            "title",
            "kit_plan_category",
            "short_description",
            "details",
            "price",
            "business_volume",
            "earnings_cap",
            "allow_repurchase",
            "can_be_upgraded",
        )

    def get_details(self, instance):
        ordered_details = instance.details.order_by("position")
        return [detail.description for detail in ordered_details]


class BlockchainChoicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlockchainChoices
        fields = ("pk", "name")


class ExchangeChoicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExchangeChoices
        fields = ("pk", "name")


class BusinessWalletSerializer(serializers.ModelSerializer):
    blockchain = serializers.SlugRelatedField(read_only=True, slug_field="name")
    exchange = serializers.SlugRelatedField(read_only=True, slug_field="name")
    type = serializers.SlugRelatedField(read_only=True, slug_field="name")
    qr_code = serializers.ImageField(use_url=True, allow_empty_file=True)

    class Meta:
        model = BusinessWallet
        fields = ("pk", "hash", "blockchain", "exchange", "type", "qr_code", "enabled")