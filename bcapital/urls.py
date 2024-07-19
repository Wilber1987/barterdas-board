"""bcapital URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from knox import views as knox_views
from transactions.views import router as transactions_router

from barter_auth.views import RegisterAPIView, LoginAPIView, router as users_router, CheckEmailAPIView, \
    ChangePasswordAPIView, ActivateUserAPIView, RecoveryPasswordAPIView

from django.urls import include, re_path

from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from django.conf import settings

import barter_auth.v2.urls
import global_settings.v2.urls
import transactions.v2.urls
import sales_funnel.v2.urls

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),

    # API v0
    path('api/register/', RegisterAPIView.as_view(), name='register-view'),
    path('api/activate/', ActivateUserAPIView.as_view(), name='activate-view'),
    path('api/users/check_email/', CheckEmailAPIView.as_view(), name='check-email'),
    path('api/users/change_password/', ChangePasswordAPIView.as_view(), name='change-password'),
    path('api/recovery_password/', RecoveryPasswordAPIView.as_view(), name='recovery-password'),
    path('api/login/', LoginAPIView.as_view(), name='login-view'),
    path('api/logout/', knox_views.LogoutView.as_view(), name='logout-view'),
    path('api/logoutall/', knox_views.LogoutAllView.as_view(), name='logoutall-view'),
    path('', include(transactions_router.urls)),
    path('', include(users_router.urls)),

    # Include the URLs for version 2 of the API from each app
    path('api/v2/barter_auth/', include('barter_auth.v2.urls')),
    path('api/v2/transactions/', include('transactions.v2.urls')),
    path('api/v2/kyc_verifications/', include('kyc_verifications.v2.urls')),
    path('api/v2/sales_funnel/', include('sales_funnel.v2.urls')),
    path('api/v2/global_settings/', include('global_settings.v2.urls')),
]

# Include DRF-Spectacular's view for schema and documentation
if settings.DEBUG:
    urlpatterns += [
        # DRF Spectacular Schema pattern
        path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
        # Optional UI:
        path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
        path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    ]