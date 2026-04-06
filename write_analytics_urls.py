with open('apps/analytics/urls.py', 'w') as f:
    f.write('from django.urls import path\n')
    f.write('from .views import DashboardStatsView, VerificationStatsView, AlertStatsView\n\n')
    f.write('urlpatterns = [\n')
    f.write('    path("dashboard/", DashboardStatsView.as_view(), name="dashboard-stats"),\n')
    f.write('    path("verifications/", VerificationStatsView.as_view(), name="verification-stats"),\n')
    f.write('    path("alerts/", AlertStatsView.as_view(), name="alert-stats"),\n')
    f.write(']\n')
print('Done')
