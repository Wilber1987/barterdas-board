"""Module for defining all of barter_auth app's serializers"""

from rest_framework import serializers
from django.core.validators import RegexValidator
from django.contrib.auth.hashers import make_password

from drf_spectacular.utils import (
    OpenApiExample,
    extend_schema_serializer,
    extend_schema_field,
)

from drf_spectacular.types import OpenApiTypes

from barter_auth.models import (
    BarterUser,
    UserWallet,
    BarterUserSecurityProfile,
    UnilevelNetwork,
)

from barter_auth.helpers import add_user_to_network


# region Auth
class UserLoginSerializer(serializers.ModelSerializer):
    """Serializer used to add to the response of the
    /login endpoint.
    Aditional fields used for sales funnel login"""

    full_name = serializers.SerializerMethodField()
    has_funnel = serializers.BooleanField(read_only=True, source="has_sales_funnel")
    funnel_username = serializers.CharField(
        read_only=True, source="sales_funnel.first().username"
    )

    class Meta:
        """Define the serializer model and fields to use"""

        model = BarterUser
        fields = [
            "id",
            "email",
            "username",
            "full_name",
            "has_funnel",
            "funnel_username",
        ]

    def get_full_name(self, instance) -> str:
        """Returns the user's full name to the method serializer"""

        return instance.full_name

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        funnel = instance.sales_funnel.filter(enabled=True).first()

        if funnel:
            ret["funnel_username"] = funnel.username
        else:
            ret["funnel_username"] = None
        return ret


class LoginSerializer(serializers.Serializer):
    """Serializer used for the request data
    of the /login endpoint"""

    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)

    token = serializers.CharField(read_only=True)
    expiry = serializers.DateTimeField(read_only=True)
    user = UserLoginSerializer(read_only=True)


# endregion


# region Users
# Serializer for registering a user with a BarterUser model
class UserCreateSerializer(serializers.ModelSerializer):
    """Serializer used for the register endpoint"""

    referral_code = serializers.CharField(allow_blank=True)
    terms_and_conditions_accepted = serializers.BooleanField(
        write_only=True, required=True
    )

    class Meta:
        """Define the serializer models and fields"""

        model = BarterUser
        fields = [
            "id",
            "first_name",
            "last_name",
            "username",
            "email",
            "password",
            "phone_number",
            "country",
            "city",
            "address",
            "zip_code",
            "referral_code",
            "terms_and_conditions_accepted",
        ]

        extra_kwargs = {
            "first_name": {"required": True},
            "last_name": {"required": True},
            "username": {"required": True},
            "email": {"required": True},
            "phone_number": {"required": True},
            "country": {"required": True},
            "city": {"required": True},
            "address": {"required": True},
            "zip_code": {"required": True},
            "password": {"write_only": True},
        }

    def create(self, validated_data) -> BarterUser:
        referred_by_code = validated_data.pop("referral_code")

        validated_data.pop("terms_and_conditions_accepted")
        validated_data["password"] = make_password(validated_data["password"])

        referred_by = None

        if referred_by_code:
            referred_by = BarterUser.objects.filter(
                referral_code=referred_by_code
            ).first()

        return BarterUser.objects.create(referred_by=referred_by, **validated_data)

    def validate_referral_code(self, value):
        """Validate if an user exists for a given referral code"""

        if value:
            try:
                BarterUser.objects.get(referral_code=value)
            except BarterUser.DoesNotExist:
                raise serializers.ValidationError("Referral code does not exist")

        return value

    def validate_terms_and_conditions_accepted(self, value):
        """Validate that the user accepts the terms and conditions"""

        if not value:
            raise serializers.ValidationError("Terms and conditions must be accepted")

        return value


class UserDetailSerializer(serializers.ModelSerializer):
    """Serializer used for the /uesrs/<id> endpoint"""

    class Meta:
        """Define the serializer model and fields"""

        model = BarterUser
        fields = [
            "id",
            "first_name",
            "last_name",
            "username",
            "email",
            "phone_number",
            "country",
            "city",
            "address",
            "zip_code",
            "referral_code",
        ]
        extra_kwargs = {
            "id": {"read_only": True},
            "referral_code": {"read_only": True},
            "username": {"read_only": True},
        }


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer for the /users/<id>/profile endpoint"""

    phone_number = serializers.CharField(
        validators=[
            RegexValidator(
                regex=r"^\+?[1-9]\d{1,14}$",  # * E.164 format with optional "+" sign
                message="Formato de número de teléfono incorrecto ('+' opcional, seguido de dígitos)",
            )
        ]
    )
    referral_link = serializers.SerializerMethodField(read_only=True)

    def get_referral_link(self, instance):
        """ "Returns an user referral link to share"""

        # TODO: Replace hardcoded string with settings parameter
        return f"https://bartercapital-dashboard.com /#/auth/register?referral_code={instance.referral_code}"

    class Meta:
        """Define the serializer's model and fields"""

        model = BarterUser
        fields = [
            "id",
            "first_name",
            "last_name",
            "username",
            "email",
            "phone_number",
            "country",
            "city",
            "address",
            "zip_code",
            "referral_code",
            "referral_link",
        ]
        extra_kwargs = {
            "id": {"read_only": True},
            "first_name": {"read_only": True},
            "last_name": {"read_only": True},
            "username": {"read_only": True},
            "email": {"read_only": True},
            "country": {"read_only": True},
            "city": {"read_only": True},
            "address": {"read_only": True},
            "zip_code": {"read_only": True},
            "referral_code": {"read_only": True},
        }


@extend_schema_serializer(many=True)
class UnilevelNetworkListSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    first_name = serializers.SerializerMethodField()
    last_name = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()

    class Meta:
        model = UnilevelNetwork
        fields = ["username", "first_name", "last_name", "email", "level"]

    def get_username(self, instance) -> str:
        return instance.user_in_network.username

    def get_first_name(self, instance) -> str:
        return instance.user_in_network.first_name

    def get_last_name(self, instance) -> str:
        return instance.user_in_network.last_name

    @extend_schema_field(OpenApiTypes.EMAIL)
    def get_email(self, instance):
        return instance.user_in_network.email


# endregion


# region UserWallet
# Serializer for registering a user with a UserWallet model
class UserWalletSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    blockchain = serializers.SlugRelatedField(read_only=True, slug_field="name")
    exchange = serializers.SlugRelatedField(read_only=True, slug_field="name")

    class Meta:
        model = UserWallet
        fields = ("pk", "user", "hash", "blockchain", "exchange")


@extend_schema_serializer(many=False, exclude_fields=["user"])
class CreateUserWalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserWallet
        fields = ("user", "hash", "blockchain", "exchange")


# endregion