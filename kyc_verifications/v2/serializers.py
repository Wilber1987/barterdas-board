import json
from rest_framework import serializers
from django.db.models import Value
from django.db.models.functions import Lower, Replace
from barter_auth.models import BarterUser
from kyc_verifications.models import (
    KYCVerificationResult,
    KYCReviewResult,
    KYCManualVerificationDetail,
)


class KYCGetAccessTokenSerializer(serializers.Serializer):
    user_email = serializers.EmailField(write_only=True)
    level_name = serializers.CharField(max_length=255, write_only=True)

    access_token = serializers.CharField(max_length=255, read_only=True)

    def validate_level_name(self, value):
        if value != "basic-kyc-level":
            raise serializers.ValidationError("Invalid level name")

        return value

    def validate_user_email(self, value):
        request = self.context.get("request")

        if request and request.user.email.lower().strip() != value.lower().strip():
            raise serializers.ValidationError("User email does not match")

        if (
            BarterUser.objects.annotate(
                lowered_nospace_email=Lower(Replace("email", Value(" "), Value("")))
            )
            .filter(lowered_nospace_email=value.lower().strip())
            .first()
            is not None
        ):
            return value.lower().strip()
        else:
            raise serializers.ValidationError("Invalid value for user_email")


class KYCReviewResultsSerializer(serializers.ModelSerializer):
    # https://developers.sumsub.com/api-reference/#getting-verification-results
    moderationComment = serializers.CharField(
        source="moderation_comment", required=False
    )
    clientComment = serializers.CharField(source="client_comment", required=False)
    reviewAnswer = serializers.CharField(source="review_answer")
    rejectLabels = serializers.ListField(required=False)
    reviewRejectType = serializers.CharField(
        source="review_reject_type", required=False
    )

    class Meta:
        model = KYCReviewResult
        fields = [
            "moderationComment",
            "clientComment",
            "reviewAnswer",
            "rejectLabels",
            "reviewRejectType",
        ]


class KYCVerificationResultSerializer(serializers.ModelSerializer):
    # https://developers.sumsub.com/api-reference/#webhook-types
    applicantId = serializers.CharField(source="applicant_id")
    inspectionId = serializers.CharField(source="inspection_id")
    correlationId = serializers.CharField(source="correlation_id")
    externalUserId = serializers.CharField(source="external_user_id")
    levelName = serializers.CharField(source="level_name", required=False)
    reviewStatus = serializers.CharField(source="review_status")
    createdAtMs = serializers.DateTimeField(source="created_at_ms")

    reviewResult = KYCReviewResultsSerializer(required=False)

    class Meta:
        model = KYCVerificationResult
        fields = [
            "applicantId",
            "inspectionId",
            "correlationId",
            "externalUserId",
            "levelName",
            "type",
            "reviewStatus",
            "createdAtMs",
            "reviewResult",
        ]

    def create(self, validated_data):
        validated_data["json_data"] = json.dumps(validated_data.copy(), default=str)
        review_result_data = validated_data.pop("reviewResult")

        reject_labels = ""

        if "rejectLabels" in review_result_data:
            for label in review_result_data["rejectLabels"]:
                reject_labels = f"{reject_labels}, {label}"

            del review_result_data["rejectLabels"]

        review_result_data["reject_labels"] = reject_labels

        verification_result = KYCVerificationResult.objects.create(**validated_data)
        review_result_data["verification_result"] = verification_result
        KYCReviewResult.objects.create(**review_result_data)

        return verification_result


class KYCManualVerificationDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = KYCManualVerificationDetail
        fields = [
            "external_user_id",
            "applicant_id",
            "level_name",
            "review_status",
            "review_answer",
        ]
