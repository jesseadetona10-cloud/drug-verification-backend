with open('apps/alerts/urls.py', 'w') as f:
    f.write('from django.urls import path\n')
    f.write('from .views import AlertListCreateView, AlertDetailView, ResolveAlertView\n\n')
    f.write('urlpatterns = [\n')
    f.write('    path("", AlertListCreateView.as_view(), name="alert-list"),\n')
    f.write('    path("<uuid:pk>/", AlertDetailView.as_view(), name="alert-detail"),\n')
    f.write('    path("<uuid:pk>/resolve/", ResolveAlertView.as_view(), name="alert-resolve"),\n')
    f.write(']\n')
print('Done')
