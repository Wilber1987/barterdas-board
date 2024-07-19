"""Module to test all of transactions app functions"""

import datetime
import pytest
import pytz
from rest_framework import status
from django.db.models import Sum

from barter_auth.models import BarterUser
from transactions.models import (
    Transaction,
    CoFounderEarningByTrading,
    DetailCoFounderEarningByTrading,
    CoFounderEarningByProducts,
    DetailCoFounderEarningByProducts,
)


class TestCofounderEarningTradingSignal:
    @pytest.mark.django_db
    def test_with_no_transactions(self, default_leadership_pool):
        user = BarterUser.objects.create(
            username="john",
            email="john@bartercapital-group.com",
            first_name="john",
            last_name="smith",
            leadership_pool_type=default_leadership_pool.filter(name="L1").first(),
        )

        CoFounderEarningByTrading.objects.create(
            leadership_pool_type=default_leadership_pool.filter(name="L1").first(),
            earning_percentage=0.1,
            month=1,
            year=2023,
        )

        CoFounderEarningByTrading.objects.create(
            leadership_pool_type=default_leadership_pool.filter(name="L1").first(),
            earning_percentage=0.1,
            month=2,
            year=2023,
        )

        CoFounderEarningByTrading.objects.create(
            leadership_pool_type=default_leadership_pool.filter(name="L1").first(),
            earning_percentage=0.1,
            month=3,
            year=2023,
        )

        assert DetailCoFounderEarningByTrading.objects.count() == 0
        assert (
            DetailCoFounderEarningByTrading.objects.filter(user=user)
            .all()
            .aggregate(Sum("earnings"))["earnings__sum"]
            is None
        )

    @pytest.mark.django_db
    def test_with_transactions(self, default_leadership_pool):
        user = BarterUser.objects.create(
            username="john",
            email="john@bartercapital-group.com",
            first_name="john",
            last_name="smith",
            leadership_pool_type=default_leadership_pool.filter(name="L1").first(),
        )

        Transaction.objects.create(
            user=user,
            wallet_address="-",
            voucher_screenshot="-",
            wallet_provider="binance",
            transaction_hash="-",
            transaction_status=1,
            description="Initial investment",
            amount=1000,
            co_founder_invest=True,
            transaction_type="co-founder",
            wallet_deposit_date=datetime.datetime(2022, 12, 1, tzinfo=pytz.UTC),
        )

        CoFounderEarningByTrading.objects.create(
            leadership_pool_type=default_leadership_pool.filter(name="L1").first(),
            earning_percentage=0.1,
            month=1,
            year=2023,
        )

        CoFounderEarningByTrading.objects.create(
            leadership_pool_type=default_leadership_pool.filter(name="L1").first(),
            earning_percentage=0.1,
            month=2,
            year=2023,
        )

        CoFounderEarningByTrading.objects.create(
            leadership_pool_type=default_leadership_pool.filter(name="L1").first(),
            earning_percentage=0.1,
            month=3,
            year=2023,
        )

        assert DetailCoFounderEarningByTrading.objects.count() == 3
        assert (
            DetailCoFounderEarningByTrading.objects.filter(user=user)
            .all()
            .aggregate(Sum("earnings"))["earnings__sum"]
            == 300
        )

    # TODO: Add earnings to reinvest
    # @pytest.mark.django_db
    # def test_with_transactions_and_reinvestments(self, default_leadership_pool):
    #     user = BarterUser.objects.create(
    #         username="john",
    #         email="john@bartercapital-group.com",
    #         first_name="john",
    #         last_name="smith",
    #         leadership_pool_type=default_leadership_pool.filter(name="L1").first(),
    #     )

    #     Transaction.objects.create(
    #         user=user,
    #         wallet_address="-",
    #         voucher_screenshot="-",
    #         wallet_provider="binance",
    #         transaction_hash="-",
    #         transaction_status=1,
    #         description="Initial investment",
    #         amount=1000,
    #         co_founder_invest=True,
    #         transaction_type="co-founder",
    #         wallet_deposit_date=datetime.datetime(2022, 12, 1, tzinfo=pytz.UTC),
    #     )

    #     ReInvestments.objects.create(
    #         user=user,
    #         amount=1000,
    #         type_re_investment='Co-Founder',
    #         created_at=datetime.datetime(2022, 12, 1, tzinfo=pytz.UTC)
    #     )

    #     CoFounderEarningByTrading.objects.create(
    #         leadership_pool_type=default_leadership_pool.filter(name="L1").first(),
    #         earning_percentage=0.1,
    #         month=1,
    #         year=2023,
    #     )

    #     CoFounderEarningByTrading.objects.create(
    #         leadership_pool_type=default_leadership_pool.filter(name="L1").first(),
    #         earning_percentage=0.1,
    #         month=2,
    #         year=2023,
    #     )

    #     CoFounderEarningByTrading.objects.create(
    #         leadership_pool_type=default_leadership_pool.filter(name="L1").first(),
    #         earning_percentage=0.1,
    #         month=3,
    #         year=2023,
    #     )

    #     assert DetailCoFounderEarningByTrading.objects.count() == 3
    #     assert (
    #         DetailCoFounderEarningByTrading.objects.filter(user=user)
    #         .all()
    #         .aggregate(Sum("earnings"))["earnings__sum"]
    #         == 600
    #     )

    @pytest.mark.django_db
    def test_with_different_leadership_pool_type(self, default_leadership_pool):
        user = BarterUser.objects.create(
            username="john",
            email="john@bartercapital-group.com",
            first_name="john",
            last_name="smith",
            leadership_pool_type=default_leadership_pool.filter(name="L1").first(),
        )

        Transaction.objects.create(
            user=user,
            wallet_address="-",
            voucher_screenshot="-",
            wallet_provider="binance",
            transaction_hash="-",
            transaction_status=1,
            description="Initial investment",
            amount=1000,
            co_founder_invest=True,
            transaction_type="co-founder",
            wallet_deposit_date=datetime.datetime(2022, 12, 1, tzinfo=pytz.UTC),
        )

        CoFounderEarningByTrading.objects.create(
            leadership_pool_type=default_leadership_pool.filter(name="L2").first(),
            earning_percentage=0.1,
            month=1,
            year=2023,
        )

        CoFounderEarningByTrading.objects.create(
            leadership_pool_type=default_leadership_pool.filter(name="L2").first(),
            earning_percentage=0.1,
            month=2,
            year=2023,
        )

        CoFounderEarningByTrading.objects.create(
            leadership_pool_type=default_leadership_pool.filter(name="L3").first(),
            earning_percentage=0.1,
            month=3,
            year=2023,
        )

        assert DetailCoFounderEarningByTrading.objects.count() == 0
        assert (
            DetailCoFounderEarningByTrading.objects.filter(user=user)
            .all()
            .aggregate(Sum("earnings"))["earnings__sum"]
            is None
        )

    @pytest.mark.django_db
    def test_with_transactions_post_earning_date(self, default_leadership_pool):
        user = BarterUser.objects.create(
            username="john",
            email="john@bartercapital-group.com",
            first_name="john",
            last_name="smith",
            leadership_pool_type=default_leadership_pool.filter(name="L1").first(),
        )

        Transaction.objects.create(
            user=user,
            wallet_address="-",
            voucher_screenshot="-",
            wallet_provider="binance",
            transaction_hash="-",
            transaction_status=1,
            description="Initial investment",
            amount=1000,
            co_founder_invest=True,
            transaction_type="co-founder",
            wallet_deposit_date=datetime.datetime(2023, 6, 1, tzinfo=pytz.UTC),
        )

        CoFounderEarningByTrading.objects.create(
            leadership_pool_type=default_leadership_pool.filter(name="L1").first(),
            earning_percentage=0.1,
            month=1,
            year=2023,
        )

        assert DetailCoFounderEarningByTrading.objects.count() == 0
        assert (
            DetailCoFounderEarningByTrading.objects.filter(user=user)
            .all()
            .aggregate(Sum("earnings"))["earnings__sum"]
            is None
        )

    @pytest.mark.django_db
    def test_with_transactions_post_create_earnings(self, default_leadership_pool):
        user = BarterUser.objects.create(
            username="john",
            email="john@bartercapital-group.com",
            first_name="john",
            last_name="smith",
            leadership_pool_type=default_leadership_pool.filter(name="L1").first(),
        )

        CoFounderEarningByTrading.objects.create(
            leadership_pool_type=default_leadership_pool.filter(name="L1").first(),
            earning_percentage=0.1,
            month=1,
            year=2023,
        )

        CoFounderEarningByTrading.objects.create(
            leadership_pool_type=default_leadership_pool.filter(name="L1").first(),
            earning_percentage=0.1,
            month=2,
            year=2023,
        )

        CoFounderEarningByTrading.objects.create(
            leadership_pool_type=default_leadership_pool.filter(name="L1").first(),
            earning_percentage=0.1,
            month=3,
            year=2023,
        )

        Transaction.objects.create(
            user=user,
            wallet_address="-",
            voucher_screenshot="-",
            wallet_provider="binance",
            transaction_hash="-",
            transaction_status=1,
            description="Initial investment",
            amount=1000,
            co_founder_invest=True,
            transaction_type="co-founder",
            wallet_deposit_date=datetime.datetime(2022, 12, 1, tzinfo=pytz.UTC),
        )

        assert DetailCoFounderEarningByTrading.objects.count() == 3
        assert (
            DetailCoFounderEarningByTrading.objects.filter(user=user)
            .all()
            .aggregate(Sum("earnings"))["earnings__sum"]
            == 300
        )

    # TODO: Add earnings to reinvest
    # @pytest.mark.django_db
    # def test_with_transactions_and_reinvestments_post_create_earnings(self, default_leadership_pool):
    #     user = BarterUser.objects.create(
    #         username="john",
    #         email="john@bartercapital-group.com",
    #         first_name="john",
    #         last_name="smith",
    #         leadership_pool_type=default_leadership_pool.filter(name="L1").first(),
    #     )

    #     CoFounderEarningByTrading.objects.create(
    #         leadership_pool_type=default_leadership_pool.filter(name="L1").first(),
    #         earning_percentage=0.1,
    #         month=1,
    #         year=2023,
    #     )

    #     CoFounderEarningByTrading.objects.create(
    #         leadership_pool_type=default_leadership_pool.filter(name="L1").first(),
    #         earning_percentage=0.1,
    #         month=2,
    #         year=2023,
    #     )

    #     CoFounderEarningByTrading.objects.create(
    #         leadership_pool_type=default_leadership_pool.filter(name="L1").first(),
    #         earning_percentage=0.1,
    #         month=3,
    #         year=2023,
    #     )

    #     Transaction.objects.create(
    #         user=user,
    #         wallet_address="-",
    #         voucher_screenshot="-",
    #         wallet_provider="binance",
    #         transaction_hash="-",
    #         transaction_status=1,
    #         description="Initial investment",
    #         amount=1000,
    #         co_founder_invest=True,
    #         transaction_type="co-founder",
    #         wallet_deposit_date=datetime.datetime(2022, 12, 1, tzinfo=pytz.UTC),
    #     )

    #     ReInvestments.objects.create(
    #         user=user,
    #         amount=1000,
    #         type_re_investment='Co-Founder',
    #         created_at=datetime.datetime(2022, 12, 1, tzinfo=pytz.UTC)
    #     )

    #     assert DetailCoFounderEarningByTrading.objects.count() == 3
    #     assert (
    #         DetailCoFounderEarningByTrading.objects.filter(user=user)
    #         .all()
    #         .aggregate(Sum("earnings"))["earnings__sum"]
    #         == 600
    #     )


class TestCofounderEarningProductSignal:
    @pytest.mark.django_db
    def test_with_no_transactions(self, default_leadership_pool):
        user = BarterUser.objects.create(
            username="john",
            email="john@bartercapital-group.com",
            first_name="john",
            last_name="smith",
            leadership_pool_type=default_leadership_pool.filter(name="L1").first(),
        )

        CoFounderEarningByProducts.objects.create(
            leadership_pool_type=default_leadership_pool.filter(name="L1").first(),
            earning_percentage=0.1,
            month=1,
            year=2023,
            product=0,
        )

        CoFounderEarningByProducts.objects.create(
            leadership_pool_type=default_leadership_pool.filter(name="L1").first(),
            earning_percentage=0.1,
            month=2,
            year=2023,
            product=0,
        )

        CoFounderEarningByProducts.objects.create(
            leadership_pool_type=default_leadership_pool.filter(name="L1").first(),
            earning_percentage=0.1,
            month=3,
            year=2023,
            product=0,
        )

        assert DetailCoFounderEarningByProducts.objects.count() == 0
        assert (
            DetailCoFounderEarningByProducts.objects.filter(user=user)
            .all()
            .aggregate(Sum("earnings"))["earnings__sum"]
            is None
        )

    @pytest.mark.django_db
    def test_with_transactions(self, default_leadership_pool):
        user = BarterUser.objects.create(
            username="john",
            email="john@bartercapital-group.com",
            first_name="john",
            last_name="smith",
            leadership_pool_type=default_leadership_pool.filter(name="L1").first(),
        )

        Transaction.objects.create(
            user=user,
            wallet_address="-",
            voucher_screenshot="-",
            wallet_provider="binance",
            transaction_hash="-",
            transaction_status=1,
            description="Initial investment",
            amount=1000,
            co_founder_invest=True,
            transaction_type="co-founder",
            wallet_deposit_date=datetime.datetime(2022, 12, 1, tzinfo=pytz.UTC),
        )

        CoFounderEarningByProducts.objects.create(
            leadership_pool_type=default_leadership_pool.filter(name="L1").first(),
            earning_percentage=0.1,
            month=1,
            year=2023,
            product=0,
        )

        CoFounderEarningByProducts.objects.create(
            leadership_pool_type=default_leadership_pool.filter(name="L1").first(),
            earning_percentage=0.1,
            month=2,
            year=2023,
            product=0,
        )

        CoFounderEarningByProducts.objects.create(
            leadership_pool_type=default_leadership_pool.filter(name="L1").first(),
            earning_percentage=0.1,
            month=3,
            year=2023,
            product=0,
        )

        assert DetailCoFounderEarningByProducts.objects.count() == 3
        assert (
            DetailCoFounderEarningByProducts.objects.filter(user=user)
            .all()
            .aggregate(Sum("earnings"))["earnings__sum"]
            == 300
        )

    # TODO: Add earnings to reinvest
    # @pytest.mark.django_db
    # def test_with_transactions_and_reinvestments(self, default_leadership_pool):

    @pytest.mark.django_db
    def test_with_different_leadership_pool_type(self, default_leadership_pool):
        user = BarterUser.objects.create(
            username="john",
            email="john@bartercapital-group.com",
            first_name="john",
            last_name="smith",
            leadership_pool_type=default_leadership_pool.filter(name="L1").first(),
        )

        Transaction.objects.create(
            user=user,
            wallet_address="-",
            voucher_screenshot="-",
            wallet_provider="binance",
            transaction_hash="-",
            transaction_status=1,
            description="Initial investment",
            amount=1000,
            co_founder_invest=True,
            transaction_type="co-founder",
            wallet_deposit_date=datetime.datetime(2022, 12, 1, tzinfo=pytz.UTC),
        )

        CoFounderEarningByProducts.objects.create(
            leadership_pool_type=default_leadership_pool.filter(name="L2").first(),
            earning_percentage=0.1,
            month=1,
            year=2023,
            product=0,
        )

        CoFounderEarningByProducts.objects.create(
            leadership_pool_type=default_leadership_pool.filter(name="L2").first(),
            earning_percentage=0.1,
            month=2,
            year=2023,
            product=0,
        )

        CoFounderEarningByProducts.objects.create(
            leadership_pool_type=default_leadership_pool.filter(name="L3").first(),
            earning_percentage=0.1,
            month=3,
            year=2023,
            product=0,
        )

        assert DetailCoFounderEarningByProducts.objects.count() == 0
        assert (
            DetailCoFounderEarningByProducts.objects.filter(user=user)
            .all()
            .aggregate(Sum("earnings"))["earnings__sum"]
            is None
        )

    @pytest.mark.django_db
    def test_with_transactions_post_earning_date(self, default_leadership_pool):
        user = BarterUser.objects.create(
            username="john",
            email="john@bartercapital-group.com",
            first_name="john",
            last_name="smith",
            leadership_pool_type=default_leadership_pool.filter(name="L1").first(),
        )

        Transaction.objects.create(
            user=user,
            wallet_address="-",
            voucher_screenshot="-",
            wallet_provider="binance",
            transaction_hash="-",
            transaction_status=1,
            description="Initial investment",
            amount=1000,
            co_founder_invest=True,
            transaction_type="co-founder",
            wallet_deposit_date=datetime.datetime(2023, 6, 1, tzinfo=pytz.UTC),
        )

        CoFounderEarningByProducts.objects.create(
            leadership_pool_type=default_leadership_pool.filter(name="L1").first(),
            earning_percentage=0.1,
            month=1,
            year=2023,
            product=0,
        )

        assert DetailCoFounderEarningByProducts.objects.count() == 0
        assert (
            DetailCoFounderEarningByProducts.objects.filter(user=user)
            .all()
            .aggregate(Sum("earnings"))["earnings__sum"]
            is None
        )

    @pytest.mark.django_db
    def test_with_transactions_post_create_earnings(self, default_leadership_pool):
        user = BarterUser.objects.create(
            username="john",
            email="john@bartercapital-group.com",
            first_name="john",
            last_name="smith",
            leadership_pool_type=default_leadership_pool.filter(name="L1").first(),
        )

        CoFounderEarningByProducts.objects.create(
            leadership_pool_type=default_leadership_pool.filter(name="L1").first(),
            earning_percentage=0.1,
            month=1,
            year=2023,
            product=0,
        )

        CoFounderEarningByProducts.objects.create(
            leadership_pool_type=default_leadership_pool.filter(name="L1").first(),
            earning_percentage=0.1,
            month=2,
            year=2023,
            product=0,
        )

        CoFounderEarningByProducts.objects.create(
            leadership_pool_type=default_leadership_pool.filter(name="L1").first(),
            earning_percentage=0.1,
            month=3,
            year=2023,
            product=0,
        )

        Transaction.objects.create(
            user=user,
            wallet_address="-",
            voucher_screenshot="-",
            wallet_provider="binance",
            transaction_hash="-",
            transaction_status=1,
            description="Initial investment",
            amount=1000,
            co_founder_invest=True,
            transaction_type="co-founder",
            wallet_deposit_date=datetime.datetime(2022, 12, 1, tzinfo=pytz.UTC),
        )

        assert DetailCoFounderEarningByProducts.objects.count() == 3
        assert (
            DetailCoFounderEarningByProducts.objects.filter(user=user)
            .all()
            .aggregate(Sum("earnings"))["earnings__sum"]
            == 300
        )

    # TODO: Add earnings to reinvest
    # @pytest.mark.django_db
    # def test_with_transactions_and_reinvestments_post_create_earnings(self, default_leadership_pool):
