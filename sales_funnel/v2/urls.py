from rest_framework import routers
from django.urls import re_path, path, include
from sales_funnel.v2.views import FunnelViewset, NewsletterSubscriptionViewset, FunnelStepList, FunnelStepDetail
from knox import views as knox_views

router = routers.SimpleRouter()
router.register(r'funnels',
                FunnelViewset,
                basename=FunnelViewset.name)
router.register(r'funnels/(?P<username>[^/.]+)/subscriptions',
                NewsletterSubscriptionViewset,
                basename=NewsletterSubscriptionViewset.name)


urlpatterns = [
    path('', include(router.urls)),
    re_path(r'^funnel-steps/$',
            FunnelStepList.as_view(),
            name=FunnelStepList.name),
    re_path(r'^funnel-steps/(?P<pk>[0-9]+)$',
            FunnelStepDetail.as_view(),
            name=FunnelStepDetail.name),
]