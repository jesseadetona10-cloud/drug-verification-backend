from django.urls import path
from .views import DashboardStatsView, VerificationStatsView, AlertStatsView

urlpatterns = [
    path("dashboard/", DashboardStatsView.as_view(), name="dashboard-stats"),
    path("verifications/", VerificationStatsView.as_view(), name="verification-stats"),
    path("alerts/", AlertStatsView.as_view(), name="alert-stats"),
]
