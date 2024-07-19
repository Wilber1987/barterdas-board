import pytest
from rest_framework.test import APIClient
from global_settings.models import (
    LeadershipPoolType,
    KitPlanUnilevelPercentage,
    TradingUnilevelPercentage,
    CapsByDirectUsers,
)
from decimal import Decimal


@pytest.fixture(scope="session", name="api_client")
def api_client_fixture():
    return APIClient()


@pytest.fixture(name="default_leadership_pool")
def default_leadership_pool_fixture(request, db):
    LeadershipPoolType.objects.bulk_create(
        [
            LeadershipPoolType(
                name="L1", description="", earning_percentage=10, enabled=True
            ),
            LeadershipPoolType(
                name="L2", description="", earning_percentage=7.5, enabled=True
            ),
            LeadershipPoolType(
                name="L3", description="", earning_percentage=5, enabled=True
            ),
        ]
    )

    default_leadership_pools = LeadershipPoolType.objects.all()
    yield default_leadership_pools


@pytest.fixture(name="default_kitplan_unilevel_percentage")
def default_kitplan_unilevel_percentage_fixture(request, db):
    KitPlanUnilevelPercentage.objects.bulk_create(
        [
            KitPlanUnilevelPercentage(
                name="L1",
                description="",
                level=1,
                earnings_percentage=Decimal(0.060),
                enabled=True,
            ),
            KitPlanUnilevelPercentage(
                name="L2",
                description="",
                level=2,
                earnings_percentage=Decimal(0.050),
                enabled=True,
            ),
            KitPlanUnilevelPercentage(
                name="L3",
                description="",
                level=3,
                earnings_percentage=Decimal(0.036),
                enabled=True,
            ),
            KitPlanUnilevelPercentage(
                name="L4",
                description="",
                level=4,
                earnings_percentage=Decimal(0.020),
                enabled=True,
            ),
            KitPlanUnilevelPercentage(
                name="L5",
                description="",
                level=5,
                earnings_percentage=Decimal(0.014),
                enabled=True,
            ),
            KitPlanUnilevelPercentage(
                name="L6",
                description="",
                level=6,
                earnings_percentage=Decimal(0.008),
                enabled=True,
            ),
            KitPlanUnilevelPercentage(
                name="L7",
                description="",
                level=7,
                earnings_percentage=Decimal(0.004),
                enabled=True,
            ),
            KitPlanUnilevelPercentage(
                name="L8",
                description="",
                level=8,
                earnings_percentage=Decimal(0.004),
                enabled=True,
            ),
            KitPlanUnilevelPercentage(
                name="L9",
                description="",
                level=9,
                earnings_percentage=Decimal(0.002),
                enabled=True,
            ),
            KitPlanUnilevelPercentage(
                name="L10",
                description="",
                level=10,
                earnings_percentage=Decimal(0.002),
                enabled=True,
            ),
        ]
    )
    default_kitplan_unilevel_percentages = KitPlanUnilevelPercentage.objects.all()
    yield default_kitplan_unilevel_percentages


@pytest.fixture(name="default_trading_unilevel_percentage")
def default_trading_unilevel_percentage_fixture(request, db):
    TradingUnilevelPercentage.objects.bulk_create(
        [
            TradingUnilevelPercentage(
                name="L1",
                description="",
                level=1,
                earnings_percentage=Decimal(0.050),
                enabled=True,
            ),
            TradingUnilevelPercentage(
                name="L2",
                description="",
                level=2,
                earnings_percentage=Decimal(0.040),
                enabled=True,
            ),
        ]
    )
    default_trading_unilevel_percentages = TradingUnilevelPercentage.objects.all()
    yield default_trading_unilevel_percentages


@pytest.fixture(name="generic_kp_caps")
def generic_kp_caps_fixture(request, db):
    caps = []

    dataset = [
        {"count_of_direct_users": 0, "level_to_win": 1, "enabled": True},
        {"count_of_direct_users": 2, "level_to_win": 2, "enabled": True},
        {"count_of_direct_users": 4, "level_to_win": 3, "enabled": True},
        {"count_of_direct_users": 6, "level_to_win": 4, "enabled": True},
    ]

    for data in dataset:
        caps.append(CapsByDirectUsers.objects.create(**data))

    yield caps
