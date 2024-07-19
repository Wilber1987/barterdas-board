from rest_framework import routers
from kyc_verifications.v2 import views
from django.urls import path, include

router = routers.SimpleRouter()
router.register('get-access-token',
                views.KYCGetAccessTokenViewset,
                basename=views.KYCGetAccessTokenViewset.name)
router.register('verification-result',
                views.KYCVerificationResultViewset,
                basename=views.KYCVerificationResultViewset.name)
router.register('manual-verification',
                views.KYCManualVerificationDetailViewset,
                basename=views.KYCManualVerificationDetailViewset.name)

urlpatterns = [
    path('', include(router.urls)),
]