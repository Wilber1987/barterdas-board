from rest_framework import generics
from rest_framework import permissions

from global_settings.models import WithdrawalType, KitPlan, BlockchainChoices, ExchangeChoices, \
                                    BusinessWallet

from global_settings.v2.serializers import WithdrawalTypeSerializer, KitPlanSerializer, \
                                            BlockchainChoicesSerializer, \
                                            ExchangeChoicesSerializer, BusinessWalletSerializer


class WithdrawalTypeList(generics.ListAPIView):
    queryset = WithdrawalType.objects.filter(enabled=True)
    serializer_class = WithdrawalTypeSerializer
    name = 'withdrawaltype-list'

    authentication_classes = []
    permission_classes = [permissions.AllowAny]


class KitPlanList(generics.ListAPIView):
    queryset = KitPlan.objects.filter(enabled=True)
    serializer_class = KitPlanSerializer
    name = 'kitplan-list'

    authentication_classes = []
    permission_classes = [permissions.AllowAny]


class BlockchainChoicesList(generics.ListAPIView):
    queryset = BlockchainChoices.objects.all()
    serializer_class = BlockchainChoicesSerializer
    name = 'blockchain-list'

    authentication_classes = []
    permission_classes = [permissions.AllowAny]

class ExchangeChoicesList(generics.ListAPIView):
    queryset = ExchangeChoices.objects.all()
    serializer_class = ExchangeChoicesSerializer
    name = 'exchange-list'

    authentication_classes = []
    permission_classes = [permissions.AllowAny]

class BusinessWalletList(generics.ListAPIView):
    queryset = BusinessWallet.objects.filter(enabled=True)
    serializer_class = BusinessWalletSerializer
    name = 'businesswallet-list'

    authentication_classes = []
    permission_classes = [permissions.AllowAny]