from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/auth/", include("apps.accounts.urls")),
    path("api/drugs/", include("apps.drugs.urls")),
    path("api/verification/", include("apps.verification.urls")),
    path("api/supply-chain/", include("apps.supply_chain.urls")),
    path("api/alerts/", include("apps.alerts.urls")),
    path("api/analytics/", include("apps.analytics.urls")),
]
