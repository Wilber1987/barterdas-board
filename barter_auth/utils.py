import random
import string

from kyc_verifications.models import KYCVerificationResult


def generate_referral_code():
    letters = string.ascii_letters
    random_code = "".join(random.choice(letters) for i in range(12))
    return "BC-" + random_code


def generate_default_image():
    return "https://ui-avatars.com/api/?size=1024&name=BC?background=random"


# region user status utils
def get_kyc_status(user):
    kyc_status = {
        "has_filled_kyc": False,
        "can_fill_kyc": False,
        "has_approved_kyc_results": False,
        "has_retry_kyc_results": False,
        "has_final_kyc_results": False,
    }

    queryset = KYCVerificationResult.objects.filter(
        external_user_id=user.email.lower().strip()
    )

    kyc_status["has_filled_kyc"] = queryset.count() > 0
    kyc_status["can_fill_kyc"] = user.can_fill_kyc
    kyc_status["has_approved_kyc_results"] = (
        queryset.filter(review_result__review_answer="GREEN").exists()
        or user.kyc_manual_verification_details.filter(review_answer="GREEN").count()
        > 0
    )
    kyc_status["has_retry_kyc_results"] = queryset.filter(
        review_result__review_reject_type="RETRY"
    ).exists()
    kyc_status["has_final_kyc_results"] = queryset.filter(
        review_result__review_reject_type="FINAL"
    ).exists()

    return kyc_status


def get_account_status(user):
    account_status = {
        "username": user.username,
        "email": user.email,
        "email_verified": user.verified,
        "is_cofounder": user.is_co_founder,
        "has_active_kitplan": user.has_active_kitplan,
        "has_pending_kitplan_transaction": user.has_pending_kitplan_transaction,
        "has_trading_plan": user.has_trading_plan,
        "has_network": user.has_network,
        "has_sales_funnel": user.has_sales_funnel,
        "leadership_pool_type_id": None
        if user.leadership_pool_type is None
        else user.leadership_pool_type.id,
        "is_active": user.is_active,
        "is_staff": user.is_staff,
        "last_login": user.last_login,
        "date_joined": user.date_joined,
    }

    return account_status


# endregion
