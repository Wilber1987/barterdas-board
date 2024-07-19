import knox.auth
import django_filters.rest_framework as django_filters
from django.core.exceptions import FieldDoesNotExist
from django.utils.timezone import now
from rest_framework import generics, viewsets, mixins, permissions, pagination, filters
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.decorators import action

from transactions.models import Transaction, Withdrawal, ReInvestments
from transactions.serializers import WithdrawalSerializer
from transactions.v2.serializers import UserTransactionSerializer, UserWithdrawalSerializer, UserReinvestmentsSerializer, UserEarningGraphicSerializer
from transactions.v2.utils import calculate_accumulative_earnings

from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse

# * Some viewsets use GenericViewSet instead of ModelViewSet
# * To avoid listing disabled operations in OpenApi documentation
# * --Jeffrey


# region Pagination classes
class SmallPageNumberPagination(pagination.PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 50


# endregion


# region Filters
class TransactionFilterSet(django_filters.FilterSet):
    transaction_type = django_filters.MultipleChoiceFilter(
        choices=Transaction.TRANSACTION_TYPE
    )
    transaction_status = django_filters.MultipleChoiceFilter(
        choices=Transaction.TRANSACTION_STATUS
    )
    transaction_hash = django_filters.CharFilter(
        field_name="transaction_hash",
        lookup_expr="icontains",
        help_text="Partial or complete transaction hash to look for (case insensitive)",
    )
    transaction_date = django_filters.DateFilter(
        field_name="transaction_date",
        lookup_expr="date",
        help_text="ISO 8601 formatted transaction date",
    )
    wallet_provider = django_filters.MultipleChoiceFilter(
        choices=Transaction.TRANSACTION_WALLET
    )
    wallet_deposit_date = django_filters.DateFilter(
        field_name="wallet_deposit_date",
        lookup_expr="date",
        help_text="ISO 8601 formatted wallet deposit date",
    )

    class Meta:
        model = Transaction
        fields = [
            "transaction_type",
            "transaction_status",
            "transaction_hash",
            "transaction_date",
            "wallet_provider",
            "wallet_deposit_date",
        ]

# endregion

#region base viewset
class UserBasedViewSet(viewsets.GenericViewSet):
    """Abstract class for restrict ViewSet queryset per User"""    
    def get_queryset(self):
        """This will only allow an user to read it's
        transaction details and not other user's transactions"""
        user = self.request.user
        
        # If the queryset doesn't contain the user field, return 'None'.
        # NOTE: It's better to return an exception that better explains the situation instead of returning 'None'.
        try:  rv = self.queryset.filter(user=user)
        except (TypeError, FieldDoesNotExist): rv = None

        return rv
    
    def perform_create(self, serializer):
        """This makes it impossible to insert transactions for another user"""
        serializer.save(user=self.request.user)
#endregion


class UserTransactionViewSet(
    UserBasedViewSet,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
):
    """List or create an user's transaction\n
    Filter use: As standard HTTP get parameters\n
    Ordering use: https://www.django-rest-framework.org/api-guide/filtering/#orderingfilter"""

    queryset = Transaction.objects.all()
    serializer_class = UserTransactionSerializer
    pagination_class = SmallPageNumberPagination
    permission_classes = [permissions.IsAuthenticated]

    filter_backends = [django_filters.DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = TransactionFilterSet
    ordering_fields = [
        "amount",
        "transaction_date",
        "wallet_deposit_date",
        "created_at",
    ]
    ordering = ["-transaction_date"]


class UserEarningsViewSet(
    viewsets.GenericViewSet
):
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(parameters=[OpenApiParameter(name="year", type=int, location="query", description="Filter data by year. If not specified, the current one will be used.")],
                   responses={200: UserEarningGraphicSerializer() ,400: OpenApiResponse(description='Bad Request')})
    @action(detail=False, methods=['get'], url_path='graphic')
    def graphic(self, request):
        """Get earnings by months of the user. Each list is listed by the year specified in query params. This list is used to deliver data to the earnings graph"""
        user = self.request.user
        year = int(request.query_params.get('year')) if request.query_params.get('year') else now().year
        
        data = UserEarningGraphicSerializer(calculate_accumulative_earnings(user=user, year=year))

        return Response(data.data)


class UserWithdrawalViewSet(
    UserBasedViewSet,
    mixins.ListModelMixin,
    mixins.CreateModelMixin
):
    """View for create a new withdrawal and a view for list withdrawals made by the user"""
    
    queryset = Withdrawal.objects.all()
    serializer_class = UserWithdrawalSerializer
    pagination_class = SmallPageNumberPagination
    permission_classes = [permissions.IsAuthenticated]


class UserReinvestmentsViewSet(
    UserBasedViewSet,
    mixins.ListModelMixin,
    mixins.CreateModelMixin
):
    """View for create a new Reinvestment and a view for list reinvestments made by the user"""
    
    queryset = ReInvestments.objects.all()
    serializer_class = UserReinvestmentsSerializer
    pagination_class = SmallPageNumberPagination
    permission_classes = [permissions.IsAuthenticated]


class WithdrawalList(generics.ListCreateAPIView):
    # queryset = Withdrawal.objects.all()
    serializer_class = WithdrawalSerializer
    name = "withdrawal-list"

    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [knox.auth.TokenAuthentication]


class ApiRoot(generics.GenericAPIView):
    name = "api-root"

    def get(self, request, *args, **kwargs):
        return Response({"withdrawal": reverse(WithdrawalList.name, request=request)})