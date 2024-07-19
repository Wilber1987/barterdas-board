"""Module to test all of transactions models"""

import pytest
import datetime
import pytz
from decimal import Decimal

from django.db.models import Sum

from barter_auth.models import BarterUser, UnilevelNetwork, BarterTradingPlan
from transactions.models import (
    Transaction,
    KitPlanNetWorkEarnings,
    TradingNetWorkEarnings,
    MonthlyTradingEarnings,
)


class TestKitPlanNetworkEarningsModel:
    @pytest.mark.django_db
    def test_with_all_levels(self, default_kitplan_unilevel_percentage):
        pass


class TestTradingNetworkEarningsModel:
    @pytest.mark.django_db
    def test_with_all_levels(self, default_trading_unilevel_percentage):
        test_user = BarterUser.objects.create(
            first_name="Test",
            last_name="User",
            username="testuser",
            email="testuser@bartercapital-group.com",
            country="United States",
            zip_code="123456",
            phone_number="12345678",
            profile_image="",
            address="123 fake street",
            city="Miami",
            verified=True,
            is_co_founder=False,
            can_fill_kyc=True,
        )

        user11 = BarterUser.objects.create(
            first_name="One",
            last_name="One",
            username="test11",
            email="test11@bartercapital-group.com",
            country="United States",
            zip_code="123456",
            phone_number="12345678",
            profile_image="",
            address="123 fake street",
            city="Miami",
            verified=True,
            is_co_founder=False,
            can_fill_kyc=True,
            referred_by=test_user,
        )

        user21 = BarterUser.objects.create(
            first_name="Two",
            last_name="One",
            username="test21",
            email="test21@bartercapital-group.com",
            country="United States",
            zip_code="123456",
            phone_number="12345678",
            profile_image="",
            address="123 fake street",
            city="Miami",
            verified=True,
            is_co_founder=False,
            can_fill_kyc=True,
            referred_by=BarterUser.objects.get(email="test11@bartercapital-group.com"),
        )

        UnilevelNetwork.objects.bulk_create(
            [
                UnilevelNetwork(
                    user=test_user,
                    user_in_network=user11,
                    in_network_through=test_user,
                    level=1,
                ),
                UnilevelNetwork(
                    user=user11,
                    user_in_network=user21,
                    in_network_through=user11,
                    level=1,
                ),
                UnilevelNetwork(
                    user=test_user,
                    user_in_network=user21,
                    in_network_through=user11,
                    level=2,
                ),
            ]
        )

        t01 = Transaction.objects.create(
            user=test_user,
            wallet_address="-",
            voucher_screenshot="-",
            wallet_provider="binance",
            transaction_hash="01",
            transaction_status=1,
            description="Inversion Trading $20",
            amount=20,
            co_founder_invest=False,
            transaction_type="trading",
            transaction_network="-",
            calculated_earnings=False,
            wallet_deposit_date=datetime.datetime(
                year=2023, month=5, day=1, tzinfo=pytz.UTC
            ),
        )

        t11 = Transaction.objects.create(
            user=BarterUser.objects.get(email="test11@bartercapital-group.com"),
            wallet_address="-",
            voucher_screenshot="-",
            wallet_provider="binance",
            transaction_hash="111",
            transaction_status=1,
            description="Inversion Trading $100",
            amount=100,
            co_founder_invest=False,
            transaction_type="trading",
            transaction_network="-",
            calculated_earnings=False,
            wallet_deposit_date=datetime.datetime(
                year=2023, month=5, day=1, tzinfo=pytz.UTC
            ),
        )

        t21 = Transaction.objects.create(
            user=BarterUser.objects.get(email="test21@bartercapital-group.com"),
            wallet_address="-",
            voucher_screenshot="-",
            wallet_provider="binance",
            transaction_hash="211",
            transaction_status=1,
            description="Inversion Trading $25",
            amount=25,
            co_founder_invest=False,
            transaction_type="trading",
            transaction_network="-",
            calculated_earnings=False,
            wallet_deposit_date=datetime.datetime(
                year=2023, month=5, day=1, tzinfo=pytz.UTC
            ),
        )
        
        BarterTradingPlan.objects.create(
            user=test_user,
            trading_amount=20,
            transaction_hash='01',
            transaction=t01
        )
        
        BarterTradingPlan.objects.create(
            user=user11,
            trading_amount=100,
            transaction_hash='111',
            transaction=t11
        )
        
        BarterTradingPlan.objects.create(
            user=user21,
            trading_amount=25,
            transaction_hash='211',
            transaction=t21
        )

        print(BarterTradingPlan.objects.all())
        print(UnilevelNetwork.objects.all())
        print(TradingNetWorkEarnings.objects.all())

        MonthlyTradingEarnings.objects.create(roi=Decimal(10.00), month=6, year=2023)

        earnings_data = TradingNetWorkEarnings.objects.filter(
            unilevel_network__user=test_user,
        )

        assert (
            earnings_data.filter(level=1).aggregate(Sum("earnings"))["earnings__sum"]
            == 5
        )
        assert (
            earnings_data.filter(level=2).aggregate(Sum("earnings"))["earnings__sum"]
            == 1
        )
        assert earnings_data.aggregate(Sum("earnings"))["earnings__sum"] == 6
