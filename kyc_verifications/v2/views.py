import os
import logging  # Should be found on lambda/monitor/logs
import requests

from django.db.models import Value
from django.db.models.functions import Lower, Replace

from rest_framework import viewsets, status
from rest_framework.response import Response

from rest_framework import permissions
import knox.auth

from kyc_verifications.utils import sign_request

from kyc_verifications.v2.serializers import (
    KYCGetAccessTokenSerializer,
    KYCVerificationResultSerializer,
    KYCManualVerificationDetailSerializer,
)

from barter_auth.models import BarterUser


logger = logging.getLogger(__name__)


class KYCGetAccessTokenViewset(viewsets.ViewSet):
    authentication_classes = [knox.auth.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    serializer_class = KYCGetAccessTokenSerializer
    name = "get-access-token-v2"

    def get_serializer(self, *args, **kwargs):
        return KYCGetAccessTokenSerializer(*args, **kwargs)

    def create(self, request):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            headers = {"Content-Type": "application/json", "Content-Encoding": "utf-8"}

            params = {
                "userId": serializer.validated_data.get("user_email"),
                "levelName": serializer.validated_data.get("level_name"),
                "ttlInSecs": "600",
            }

            try:
                resp = sign_request(
                    requests.Request(
                        "POST",
                        f'{os.environ.get("SUMSUB_BASE_URL")}/resources/accessTokens',
                        params=params,
                        headers=headers,
                    )
                )
            except Exception as e:
                logger.error(f"KYC Get Access Token Sign Exception: {str(e)}")
                return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            try:
                s = requests.Session()
                response = s.send(resp, timeout=120)

                logger.info(f"{os.environ.get('SUMSUB_BASE_URL')}/resources/accessTokens response data: {response}")

                token = response.json()["token"]

                serializer.validated_data["access_token"] = token

                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except Exception as e:
                logger.error(f"KYC GEt Access Token Response Exception: {str(e)}")
                return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class KYCVerificationResultViewset(viewsets.ViewSet):
    authentication_classes = []
    permission_classes = [permissions.AllowAny]

    serializer_class = KYCVerificationResultSerializer
    name = "verification-result-v2"

    def get_serializer(self, *args, **kwargs):
        return KYCVerificationResultSerializer(*args, **kwargs)

    def create(self, request):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()

            try:
                user = (
                    BarterUser.objects.annotate(
                        lowered_nospace_email=Lower(
                            Replace("email", Value(" "), Value(""))
                        )
                    )
                    .filter(
                        lowered_nospace_email=serializer.validated_data[
                            "external_user_id"
                        ]
                    )
                    .first()
                )

                if user is not None:
                    user.can_fill_kyc = False
                    user.save()
                else:
                    logger.warning(
                        f'A KYC verification has been received from frontend that does not correlate to an existing user id ({serializer.validated_data["external_user_id"]}).'
                    )
            except Exception as e:
                logger.error(
                    f"An unexpected exception has been raised on kycmanualverificationdetail endpoint. Exception: {repr(e)}"
                )

        # Since Sumsub webhook does not require nor needs a detailed response from us
        return Response(status=status.HTTP_200_OK)


class KYCManualVerificationDetailViewset(viewsets.ViewSet):
    authentication_classes = [knox.auth.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    serializer_class = KYCManualVerificationDetailSerializer
    name = "manual-verification-v2"

    def get_serializer(self, *args, **kwargs):
        return KYCManualVerificationDetailSerializer(*args, **kwargs)

    def create(self, request):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()

            try:
                user = BarterUser.objects.get(
                    pk=int(serializer.validated_data["external_user_id"])
                )
                user.can_fill_kyc = False
                user.save()
            except BarterUser.DoesNotExist:
                logger.warning(
                    f'A KYC manual verification has been received from frontend that does not correlate to an existing user id ({serializer.validated_data["external_user_id"]}).'
                )
            except Exception as e:
                logger.error(
                    f"An unexpected exception has been raised on kycmanualverificationdetail endpoint. Exception: {repr(e)}"
                )

            return Response(status=status.HTTP_200_OK)