from abc import ABC

from rest_framework import serializers

from barter_auth.models import BarterUser, Referral, BarterPlan, BarterUserSecurityProfile, BarterTradingPlan, \
    BarterUserNode, BarterPlanCredentials


class BarterUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = BarterUser
        fields = ('id', 'username', 'email')

class BarterUserSecurityProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = BarterUserSecurityProfile
        fields = '__all__'
class BarterUserProfileSerializer(serializers.ModelSerializer):
    security_profiles = BarterUserSecurityProfileSerializer(many=True, required=False)
    class Meta:
        model = BarterUser
        fields = ('id','profile_image', 'first_name', 'last_name', 'username', 'email', 'country',
                  'zip_code', 'phone_number', 'address', 'city', 'is_active', 'has_plan',
                  'profile_registered', 'has_trading_plan', 'referral_code', 'is_co_founder',
                  'has_network', 'verified', 'security_profiles')


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = BarterUser
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = BarterUser.objects.create_user(**validated_data)
        return user


class ReferralSerializer(serializers.ModelSerializer):
    class Meta:
        model = Referral
        fields = '__all__'


class ReferralListSerializer(serializers.ModelSerializer):
    investment = BarterUserProfileSerializer()

    class Meta:
        model = Referral
        fields = ['investment', 'transaction_hash', 'amount', 'category']


class BarterPlanCredentialSerializer(serializers.ModelSerializer):
    class Meta:
        model = BarterPlanCredentials
        fields = '__all__'


class BarterPlanSerializer(serializers.ModelSerializer):
    credentials = BarterPlanCredentialSerializer(many=True, required=False)

    class Meta:
        model = BarterPlan
        fields = ['id', 'selected_plan', 'transaction_hash', 'created_at', 'expiration', 'user', 'credentials',
                  'transaction', 'plan']

        # se escriben como no requeridos para que no se pida en el serializer
        # ya que se agrega en el create del viewset
        extra_kwargs = {
            'plan': {'required': False},
            'transaction': {'required': False},
        }


class BarterUserChangePasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = BarterUser

        email = serializers.EmailField(required=True)
        new_password = serializers.CharField(required=True)
class BarterUserCheckEmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = BarterUser
        fields = ['email']


class BarterTradingPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = BarterTradingPlan
        fields = '__all__'

        extra_kwargs = {
            'plan': {'required': False},
            'transaction': {'required': False},
        }

class BarterUserNodeSerializer(serializers.ModelSerializer):
    investment = BarterUserProfileSerializer()

    class Meta:
        model = BarterUserNode
        fields = ['investment', 'category']
