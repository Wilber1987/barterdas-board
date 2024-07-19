import pytest

from barter_auth.models import BarterUser
from kyc_verifications.v2.serializers import KYCGetAccessTokenSerializer


@pytest.mark.django_db
class TestKYCGetAccessTokenSerializer:
    def test_valid_user(self):
        user = BarterUser.objects.create(
            username="jeff",
            email="jeff@bartercapital-group.com",
            password="jeff",
            first_name="jeff",
            last_name="soma",
        )

        data = {
            "user_email": user.email,
            "level_name": "basic-kyc-level",
        }

        serializer = KYCGetAccessTokenSerializer(data=data)

        assert serializer.is_valid() is True
        assert serializer.validated_data["user_email"] == user.email
        assert serializer.validated_data["level_name"] == "basic-kyc-level"

    def test_valid_user_email_different_case(self):
        user = BarterUser.objects.create(
            username="jeff",
            email="JEFF@bartercapital-group.com",
            password="jeff",
            first_name="jeff",
            last_name="soma",
        )

        data = {
            "user_email": "JeFf@BarterCapital-Group.Com",
            "level_name": "basic-kyc-level",
        }

        serializer = KYCGetAccessTokenSerializer(data=data)

        assert serializer.is_valid() is True
        assert serializer.validated_data["user_email"] == "jeff@bartercapital-group.com"
        assert serializer.validated_data["level_name"] == "basic-kyc-level"

    def test_invalid_user(self):
        data = {
            "user_email": "jeff@bartercapital-group.com",
            "level_name": "basic-kyc-level",
        }

        serializer = KYCGetAccessTokenSerializer(data=data)

        assert serializer.is_valid() is False

    def test_invalid_level_name(self):
        user = BarterUser.objects.create(
            username="jeff",
            email="jeff@bartercapital-group.com",
            password="jeff",
            first_name="jeff",
            last_name="soma",
        )

        data = {
            "user_email": user.email,
            "level_name": "fake-level",
        }

        serializer = KYCGetAccessTokenSerializer(data=data)

        assert serializer.is_valid() is False
