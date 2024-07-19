""""Module for defining all of transaction's app urls or endpoints"""
from django.urls import re_path, path, include
from rest_framework import routers
from transactions.v2.views import WithdrawalList, UserTransactionViewSet, UserWithdrawalViewSet, UserReinvestmentsViewSet, UserEarningsViewSet

router = routers.SimpleRouter()
router.register(r'user-transactions', UserTransactionViewSet)
router.register(r'user-withdrawals', UserWithdrawalViewSet)
router.register(r'user-reinvestments', UserReinvestmentsViewSet)
router.register(r'user-earnings', UserEarningsViewSet, 'user-earnings')

urlpatterns = [
    path("", include(router.urls)),
    re_path(r'^withdrawals/$',
            WithdrawalList.as_view(),
            name=WithdrawalList.name),
]