"""Module for al of barter_auth app endpoints"""
from django.contrib.auth import login
from django.core.exceptions import ObjectDoesNotExist

from knox.views import LoginView as KnoxLoginView
import knox.auth

from rest_framework.reverse import reverse
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.response import Response
from rest_framework import status, viewsets, permissions, mixins, generics
from rest_framework.throttling import UserRateThrottle
from rest_framework.decorators import action
from rest_framework.serializers import (
    BooleanField,
    CharField,
    DateTimeField,
    IntegerField,
    DecimalField,
)

from drf_spectacular.extensions import OpenApiAuthenticationExtension
from drf_spectacular.utils import (
    inline_serializer,
    extend_schema,
    extend_schema_view,
    OpenApiResponse,
    OpenApiParameter,
)

from barter_auth.models import BarterUser, UserWallet
from barter_auth.utils import get_kyc_status, get_account_status
from barter_auth.handlers import send_activate_user, activate_user
from barter_auth.v2 import utils
from barter_auth.v2.permissions import UserPermissions

from barter_auth.v2.serializers import (
    LoginSerializer,
    UserLoginSerializer,
    UserDetailSerializer,
    UserProfileSerializer,
    UserWalletSerializer,
    CreateUserWalletSerializer,
    UserCreateSerializer,
    UnilevelNetworkListSerializer,
)


from transactions.models import KitPlanNetWorkEarnings
from transactions.v2.serializers import KitPlanEarningsSerializer


# region Throttles
class BarterUserRateThrottle(UserRateThrottle):
    """ "Limit user requests to once per minute"""

    rate = "1/min"


# endregion


# region Auth and Register


class KnoxTokenScheme(OpenApiAuthenticationExtension):
    """Used for OpenAPI authentication"""

    target_class = "knox.auth.TokenAuthentication"
    name = "knoxTokenAuth"

    def get_security_definition(self, auto_schema):
        return {
            "type": "apiKey",
            "in": "header",
            "name": "Authorization",
            "description": "Token-based authentication with required prefix 'Token'",
        }


class LoginView(KnoxLoginView):
    """Login endpoint based on KnoxAuth
    https://james1345.github.io/django-rest-knox/auth/"""

    permission_classes = [
        permissions.AllowAny,
    ]
    authentication_classes = []
    serializer_class = LoginSerializer

    @extend_schema(
        request=AuthTokenSerializer,
        responses={
            200: inline_serializer(
                name="",
                fields={
                    **LoginSerializer().fields.fields,
                    "user": {**UserLoginSerializer().fields.fields},
                },
            ),
            401: OpenApiResponse(description="Unauthorized"),
        },
    )
    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data["user"]
            login(request, user)

            auth_data = super(LoginView, self).post(request, format=None).data
            user_serializer = UserLoginSerializer(user)

            user_data = {**auth_data, "user": {**user_serializer.data}}
            return Response(user_data)
        else:
            return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)


class RegisterViewset(viewsets.GenericViewSet, mixins.CreateModelMixin):
    """Register a new user"""

    queryset = BarterUser.objects.all()
    serializer_class = UserCreateSerializer

    permission_classes = [permissions.AllowAny]
    authentication_classes = []


# endregion


# region Users
class UserViewSet(viewsets.GenericViewSet):
    """Viewset for /users/<id>/ endpoint and all of it's detail actions"""

    queryset = BarterUser.objects.all()
    serializer_class = UserDetailSerializer

    permission_classes = [permissions.IsAuthenticated, UserPermissions]
    authentication_classes = [knox.auth.TokenAuthentication]

    # region actions
    @extend_schema(
        responses={
            200: inline_serializer(
                name="UserAccountStatusSerializer",
                fields={
                    "username": CharField(),
                    "email": CharField(),
                    "email_verified": CharField(),
                    "is_cofounder": BooleanField(),
                    "has_active_kitplan": BooleanField(),
                    "has_pending_kitplan_transaction": BooleanField(),
                    "has_trading_plan": BooleanField(),
                    "has_network": BooleanField(),
                    "has_sales_funnel": BooleanField(),
                    "leadership_pool_type_id": IntegerField(),
                    "is_active": BooleanField(),
                    "is_staff": BooleanField(),
                    "last_login": DateTimeField(),
                    "date_joined": DateTimeField(),
                },
            )
        }
    )
    @action(detail=True, methods=["get"], url_path="account")
    def account_status(self, request, pk=None):
        """Returns an user's account status"""

        user = self.get_object()

        if user == request.user:
            user_account_status = get_account_status(user)

            return Response(user_account_status, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)

    @action(detail=True, methods=["GET", "PATCH"], url_path="profile")
    def user_profile(self, request, pk=None):
        """Returns an user's profile and allows phone_number modification"""

        user = self.get_object()

        print(request.method)

        if user == request.user:
            if request.method == "GET":
                serializer = UserProfileSerializer(user)
                return Response(serializer.data)

            elif request.method == "PATCH":
                serializer = UserProfileSerializer(
                    user, data=request.data, partial=True
                )

                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
                else:
                    return Response(
                        serializer.errors, status=status.HTTP_400_BAD_REQUEST
                    )
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)

    @extend_schema(
        responses={
            200: inline_serializer(
                name="UserKYCStatusSerializer",
                fields={
                    "has_filled_kyc": BooleanField(),
                    "can_fill_kyc": BooleanField(),
                    "has_approved_kyc_results": BooleanField(),
                    "has_retry_kyc_results": BooleanField(),
                    "has_final_kyc_results": BooleanField(),
                },
            )
        }
    )
    @action(detail=True, methods=["get"], url_path="kyc")
    def kyc_status(self, request, pk=None):
        """Returns an user's kyc status"""

        user = self.get_object()

        if user == request.user:
            user_kyc_status = get_kyc_status(user)

            return Response(user_kyc_status, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)

    @extend_schema(
        responses={
            200: inline_serializer(
                name="UserBalanceSerializer",
                fields={
                    "trading": inline_serializer(
                        name="UserTradingBalanceSerializer",
                        fields={
                            "balance": DecimalField(
                                max_digits=10, decimal_places=2, min_value=0
                            ),
                            "current_earnings": DecimalField(
                                max_digits=10, decimal_places=2, min_value=0
                            ),
                            "current_network_earnings": DecimalField(
                                max_digits=10, decimal_places=2, min_value=0
                            ),
                            "balance_pending_approval": DecimalField(
                                max_digits=10, decimal_places=2, min_value=0
                            ),
                        },
                    ),
                    "kitplan": inline_serializer(
                        name="UserKitPlanBalanceSerializer",
                        fields={
                            "balance": DecimalField(
                                max_digits=10, decimal_places=2, min_value=0
                            ),
                            "current_network_earnings": DecimalField(
                                max_digits=10, decimal_places=2, min_value=0
                            ),
                            "balance_pending_approval": DecimalField(
                                max_digits=10, decimal_places=2, min_value=0
                            ),
                        },
                    ),
                    "cofounder": inline_serializer(
                        name="UserCoFounderBalanceSerializer",
                        fields={
                            "balance": DecimalField(
                                max_digits=10, decimal_places=2, min_value=0
                            ),
                            "current_earnings": DecimalField(
                                max_digits=10, decimal_places=2, min_value=0
                            ),
                            "balance_pending_approval": DecimalField(
                                max_digits=10, decimal_places=2, min_value=0
                            ),
                        },
                    ),
                    "total_monthly_earnings": inline_serializer(
                        name="UserMonthlyEarningsBalanceSerializer",
                        fields={
                            "balance": DecimalField(
                                max_digits=10, decimal_places=2, min_value=0
                            )
                        },
                    ),
                },
            )
        }
    )
    @action(detail=True, methods=["get"], url_path="balance")
    def user_balance(self, request, pk=None):
        """ "Returns an user's general balance"""

        user = self.get_object()

        if user == request.user:
            balance = utils.calculate_user_balance(user)

            return Response(balance)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)

    @extend_schema(
        responses={
            200: UnilevelNetworkListSerializer,
            403: OpenApiResponse(description="Forbidden"),
        }
    )
    @action(detail=True, methods=["get"], url_path="unilevel-network-list")
    def unilevel_network_list(self, request, pk=None):
        """Return's an user unilevel network list"""

        user = self.get_object()

        if user == request.user:
            data = user.unilevel_network.all()

            serializer = UnilevelNetworkListSerializer(data, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)

    @extend_schema(
        operation_id="v2_users_wallet_list",
        methods=["GET"],
        responses={200: UserWalletSerializer(many=True)},
    )
    @extend_schema(
        methods=["POST"],
        request=CreateUserWalletSerializer(),
        responses={
            201: OpenApiResponse(description="Created"),
            400: OpenApiResponse(description="Bad Request"),
        },
    )
    @action(detail=True, methods=["get", "post"], url_path="wallet")
    def user_wallet_list(self, request, pk=None):
        """returns an user list of stored wallets"""

        user = self.get_object()

        if user == request.user:
            if request.method == "GET":  # Get all wallets of the user
                serializer = UserWalletSerializer(user.wallet, many=True)
                return Response(serializer.data)

            elif request.method == "POST":
                request.data["user"] = user
                serializer = CreateUserWalletSerializer(request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(status=status.HTTP_201_CREATED)
                else:
                    return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)

    @extend_schema(
        methods=["DELETE", "GET"],
        parameters=[
            OpenApiParameter(
                name="wallet_id",
                allow_blank=False,
                required=True,
                type=int,
                location=OpenApiParameter.PATH,
            )
        ],
    )
    @extend_schema(
        operation_id="v2_users_wallet_detail",
        methods=["GET"],
        responses={200: UserWalletSerializer()},
    )
    @extend_schema(
        methods=["DELETE"], responses={204: OpenApiResponse(description="No Content")}
    )
    @action(
        detail=True, methods=["get", "delete"], url_path="wallet/(?P<wallet_id>[^/.]+)"
    )
    def user_wallet_detail(self, request, pk=None, wallet_id=None):
        user: BarterUser = self.get_object()

        try:
            wallet: UserWallet = user.wallet.get(pk=wallet_id, enabled=True)
        except UserWallet.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.method == "GET":  # Get all wallets of the user
            serializer = UserWalletSerializer(wallet, many=True)
            return Response(serializer.data)
        elif request.method == "DELETE":
            wallet.enabled = False
            wallet.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @extend_schema(
        request=None,
        responses={
            200: OpenApiResponse(
                description="A empty [ 200 | OK ] if the server tried to send the email, or the user was verified."
            ),
            404: OpenApiResponse(
                description="A empty [ 404 | Not Found ] if the value of <id> parameter doesn't corresponds to a user in the database"
            ),
            429: OpenApiResponse(
                description=f"A [ 429 | To Many Request ] with a explanation of why is temporarily blocked (This endpoint is blocked by user). Tried to use this endpoint more that once in {BarterUserRateThrottle.rate}"
            ),
        },
    )
    @action(
        detail=True,
        methods=["post"],
        url_path="send-email-verification",
        throttle_classes=[BarterUserRateThrottle],
    )
    def user_email_verification(self, request, pk=None):
        """Send email verification for a given user
        if the account is not verified"""

        user: BarterUser = self.get_object()
        if not user.verified:
            send_activate_user(user)

        return Response(status=status.HTTP_200_OK)

    @extend_schema(deprecated=True)
    @action(detail=True, methods=["get"], url_path="earnings/(?P<earning_type>[^/.]+)")
    def user_earnings_list(self, request, pk=None, earning_type=None):
        try:
            user: BarterUser = BarterUser.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if earning_type == "kit-plan":
            earning = KitPlanNetWorkEarnings.objects.filter(
                unilevel_network__in=user.unilevel_network_in.all(), enabled=True
            )
            earning_serialized = KitPlanEarningsSerializer(earning, many=True)
            return Response(earning_serialized.data)
        # ! Commented until trading network earnings is in development branch
        # elif earning_type == "trading":
        #     earning = TradingNetWorkEarnings.objects.filter(
        #         unilevel_network__in=user.unilevel_network_in.all(), enabled=True
        #     )
        #     earning_serialized = TradingEarningsSerializer(earning, many=True)
        #     return Response(earning_serialized.data)
        elif earning_type == "co-founder":
            # Pendiente
            return Response(status=status.HTTP_503_SERVICE_UNAVAILABLE)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    # endregion


# endregion


@extend_schema_view(
    post=extend_schema(
        parameters=[
            OpenApiParameter(
                "token",
                type=str,
                allow_blank=False,
                required=True,
                location=OpenApiParameter.PATH,
            )
        ],
        responses={
            200: OpenApiResponse(description="OK"),
            404: OpenApiResponse(description="Not Found"),
        },
    )
)
class ActivateUserAPIView(generics.CreateAPIView):
    """View for the /users/<id>/verify-email-token/ endpoint"""

    permission_classes = [permissions.AllowAny]
    authentication_classes = []

    def post(self, request, token, format=None):
        was_activated = activate_user(token)

        if was_activated:
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class ApiRoot(generics.GenericAPIView):
    """View for the browsable api on /api/v2/barter_auth/ endpoint"""

    name = "api-root"

    def get(self, request, *args, **kwargs):
        data = {}

        return Response(data)