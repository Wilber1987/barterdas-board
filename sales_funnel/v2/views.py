import logging

import knox.auth
from django_filters import rest_framework as filters
from drf_spectacular.utils import (
    OpenApiParameter,
    OpenApiResponse,
    extend_schema,
    extend_schema_view,
)
from rest_framework import generics, permissions, status, viewsets
from rest_framework.filters import SearchFilter
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle

from email_app.utils import send_sales_funnel_welcome_email
from sales_funnel.filters import DefaultPagination, NewsletterSubscriptionFilter
from sales_funnel.models import FunnelStep, NewsletterSubscription, SalesFunnelOwner
from sales_funnel.v2.serializers import (
    FunnelStepSerializer,
    NewsletterSubscriptionSerializer,
    SalesFunnelOwnerSerializer,
)

logger = logging.getLogger("sales_funnel")


class NewsletterSubscriptionThrottle(AnonRateThrottle):
    rate = "1/s"


@extend_schema_view(
    update=extend_schema(
        parameters=[
            OpenApiParameter(
                name="username",
                allow_blank=False,
                required=True,
                type=str,
                location=OpenApiParameter.PATH,
            )
        ],
        request=SalesFunnelOwnerSerializer,
        responses={
            200: SalesFunnelOwnerSerializer,
            400: OpenApiResponse(description="error: Invalid file extension"),
        },
    ),
    retrieve=extend_schema(
        parameters=[
            OpenApiParameter(
                name="username",
                allow_blank=False,
                required=True,
                type=str,
                location=OpenApiParameter.PATH,
            )
        ],
        responses={200: SalesFunnelOwnerSerializer},
    ),
)
class FunnelViewset(viewsets.ViewSet):
    authentication_classes = [knox.auth.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = SalesFunnelOwnerSerializer
    lookup_field = "username"
    parser_classes = (MultiPartParser, FormParser)

    name = "funnels-v2"

    # region Overriden permissions and authenticators
    def get_permissions(self):
        if self.request is not None:
            if self.request.method == "GET":
                return [permissions.AllowAny()]
            return super().get_permissions()

    def get_authenticators(self):
        if self.request is not None:
            if self.request.method == "GET":
                return []
            return super().get_authenticators()

    # endregion

    # region Overriden retrieve and update methods
    def retrieve(self, request, username=None):
        try:
            funnel = SalesFunnelOwner.objects.get(username=username)
        except SalesFunnelOwner.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        # ! HACK: Should be a parameter in the database
        # ! this implementation dosnt modify the entry in the database
        # ! HACK: Hosted on a "CDN", to be fixed for a youtube video url
        funnel.custom_video_url = "https://drive.google.com/uc?export=view&id=1fk3FRZnXeJy7d1O06DZNa3r0oBUgGL09"

        serializer = SalesFunnelOwnerSerializer(funnel)
        return Response(serializer.data)

    def update(self, request, username=None):
        try:
            funnel = SalesFunnelOwner.objects.get(username=username)
        except SalesFunnelOwner.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        file = request.FILES.get("profile_image")

        if file is not None:
            if (
                not file.name.endswith(".jpg")
                and not file.name.endswith(".jpeg")
                and not file.name.endswith(".png")
            ):
                return Response(
                    {"error": "Invalid file extension"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        serializer = SalesFunnelOwnerSerializer(funnel, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

    # endregion


@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter(
                name="username",
                allow_blank=False,
                required=True,
                type=str,
                location=OpenApiParameter.PATH,
            ),
            OpenApiParameter(
                name="subscriptor_email",
                allow_blank=False,
                required=False,
                type=str,
                location=OpenApiParameter.QUERY,
            ),
        ],
        responses={
            200: NewsletterSubscriptionSerializer(many=True),
            403: OpenApiResponse(description="Forbidden"),
        },
    ),
    create=extend_schema(
        parameters=[
            OpenApiParameter(
                name="username",
                allow_blank=False,
                required=True,
                type=str,
                location=OpenApiParameter.PATH,
            )
        ],
        request=NewsletterSubscriptionSerializer,
        responses={
            200: NewsletterSubscriptionSerializer(many=True),
            403: OpenApiResponse(description="Forbidden"),
        },
    ),
)
class NewsletterSubscriptionViewset(viewsets.ViewSet):
    queryset = NewsletterSubscription.objects.all()
    serializer_class = NewsletterSubscriptionSerializer
    authentication_classes = [knox.auth.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    throttle_classes = [NewsletterSubscriptionThrottle]
    name = "subscriptions-v2"

    filter_backends = [filters.DjangoFilterBackend, SearchFilter]
    filterset_class = NewsletterSubscriptionFilter
    search_fields = ["subscriptor_email"]

    pagination_class = DefaultPagination

    # region Overriden queryset, serializer, permissions, authenticators
    def get_queryset(self):
        username = self.kwargs.get("username")
        subscriptor_email = self.request.query_params.get("subscriptor_email")

        if username is not None:
            queryset = NewsletterSubscription.objects.filter(
                subscribed_to__username=username
            )
            if subscriptor_email is not None:
                queryset = queryset.filter(
                    subscriptor_email__icontains=subscriptor_email
                )

            return queryset

        return []

    def get_serializer(self, *args, **kwargs):
        return NewsletterSubscriptionSerializer(*args, **kwargs)

    def get_permissions(self):
        if self.request is not None:
            if self.request.method == "POST":
                return [permissions.AllowAny()]
            return super().get_permissions()

    def get_authenticators(self):
        if self.request is not None:
            if self.request.method == "POST":
                return []
            return super().get_authenticators()

    # endregion

    # region Overriden list, create
    def list(self, request, username):
        try:
            sales_funnel = SalesFunnelOwner.objects.get(username=username)
        except SalesFunnelOwner.DoesNotExist:
            return Response(status=status.HTTP_403_FORBIDDEN)

        if sales_funnel.user == request.user:
            newsletter_subscriptions = self.get_queryset()
            serializer = self.get_serializer(newsletter_subscriptions, many=True)

            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_403_FORBIDDEN)

    def create(self, request, username):
        try:
            sales_funnel = SalesFunnelOwner.objects.get(username=username)
        except SalesFunnelOwner.DoesNotExist:
            return Response(status=status.HTTP_403_FORBIDDEN)

        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save(subscribed_to=sales_funnel, sent_emails=0, enabled=True)

            try:
                send_sales_funnel_welcome_email(
                    serializer.validated_data["subscriptor_email"]
                )
            except Exception as e:
                logger.exception(
                    f"Exception: {str(e)}, Sales funnel email couldn't be sent "
                    + f"to {serializer.validated_data['subscriptor_email']}"
                )

            return Response(serializer.data, status=status.HTTP_201_CREATED)

    # endregion


class FunnelStepList(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    authentication_classes = []

    queryset = FunnelStep.objects.filter(enabled=True)
    serializer_class = FunnelStepSerializer
    name = "funnelstep-list"


class FunnelStepDetail(generics.RetrieveAPIView):
    permission_classes = [permissions.AllowAny]
    authentication_classes = []

    queryset = FunnelStep.objects.all()
    serializer_class = FunnelStepSerializer
    name = "funnelstep-detail"
