from django.urls import path
from .views import VerifyDrugView, VerificationHistoryView

urlpatterns = [
    path("verify/", VerifyDrugView.as_view(), name="verify-drug"),
    path("history/", VerificationHistoryView.as_view(), name="verification-history"),
]
