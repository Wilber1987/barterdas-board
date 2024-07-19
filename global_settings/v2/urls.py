from django.urls import re_path
from global_settings.v2 import views

urlpatterns = [
    re_path(r'^withdrawal_types/$',
            views.WithdrawalTypeList.as_view(),
            name=views.WithdrawalTypeList.name),
    re_path(r'^kitplans/$',
         	views.KitPlanList.as_view(),
            name=views.KitPlanList.name),
    re_path(r'^exchanges/$',
            views.ExchangeChoicesList.as_view(),
            name=views.ExchangeChoicesList.name),
    re_path(r'^blockchains/$',
            views.BlockchainChoicesList.as_view(),
            name=views.BlockchainChoicesList.name),
    re_path(r'^business-wallets/$',
            views.BusinessWalletList.as_view(),
            name=views.BusinessWalletList.name),
]