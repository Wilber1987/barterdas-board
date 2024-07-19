# ? Why is this in transactions?
import pytest

from barter_auth.model_utils.barteruser_utils import add_user_to_network
from barter_auth.models import BarterUser
from global_settings.models import CapsByDirectUsers
from transactions.handlers import (
    verify_cap_by_direct_users,
)


def create_user_with_unilevel(directs_amount: int):
    main_user = BarterUser.objects.create(
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

    users = []

    for i in range(directs_amount):
        users.append(
            BarterUser.objects.create(
                first_name="Test",
                last_name="User",
                username=f"testuser{i}",
                email=f"testuser{i}@bartercapital-group.com",
                country="United States",
                zip_code="123456",
                phone_number="12345678",
                profile_image="",
                address="123 fake street",
                city="Miami",
                verified=True,
                is_co_founder=False,
                can_fill_kyc=True,
                referred_by=main_user,
            )
        )

        add_user_to_network(users[i])

    return main_user


class TestKPCapsImplementation:
    @pytest.mark.django_db
    @pytest.mark.parametrize("direct_amount", [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    def test_kp_caps_per_direct_referrals_amount(generics_kp_caps, direct_amount):
        user = create_user_with_unilevel(direct_amount)

        for i in range(10):
            cap = CapsByDirectUsers.objects.filter(level_to_win=i + 1).first()

            if cap is not None:
                assert verify_cap_by_direct_users(user, i + 1) == (
                    direct_amount >= cap.count_of_direct_users
                )
