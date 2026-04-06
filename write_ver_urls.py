with open('apps/verification/urls.py', 'w') as f:
    f.write('from django.urls import path\n')
    f.write('from .views import VerifyDrugView, VerificationHistoryView\n\n')
    f.write('urlpatterns = [\n')
    f.write('    path("verify/", VerifyDrugView.as_view(), name="verify-drug"),\n')
    f.write('    path("history/", VerificationHistoryView.as_view(), name="verification-history"),\n')
    f.write(']\n')
print('Done')
