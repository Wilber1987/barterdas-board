""""Module for defining app views's urls"""
from django.urls import re_path, path, include
from rest_framework import routers

from knox import views as knox_views
from barter_auth.v2.views import (
    LoginView,
    UserViewSet,
    RegisterViewset,
    ActivateUserAPIView,
    ApiRoot
)

router = routers.SimpleRouter()
router.register(r"register", RegisterViewset)
router.register(r"users", UserViewSet)

urlpatterns = [
    path("", include(router.urls)),
    re_path(r"login", LoginView.as_view(), name="knox_login"),
    re_path(r"logout/", knox_views.LogoutView.as_view(), name="knox_logout"),
    re_path(r"logoutall/", knox_views.LogoutAllView.as_view(), name="knox_logoutall"),
    re_path(
        r"^verify-email-token/(?P<token>[\w-]+)/?$",
        ActivateUserAPIView.as_view(),
        name="verify-email-token",
    ),
    path('', ApiRoot.as_view(), name='api-root'),
]