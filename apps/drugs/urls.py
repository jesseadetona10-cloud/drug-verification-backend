from django.urls import path
from .views import DrugListCreateView, DrugDetailView, BatchListCreateView, DrugVerifyView, BatchQRCodeView, ApproveDrugView, RejectDrugView, PendingDrugsView

urlpatterns = [
    path("", DrugListCreateView.as_view(), name="drug-list"),
    path("pending/", PendingDrugsView.as_view(), name="pending-drugs"),
    path("<uuid:pk>/", DrugDetailView.as_view(), name="drug-detail"),
    path("<uuid:pk>/approve/", ApproveDrugView.as_view(), name="drug-approve"),
    path("<uuid:pk>/reject/", RejectDrugView.as_view(), name="drug-reject"),
    path("<uuid:drug_id>/batches/", BatchListCreateView.as_view(), name="batch-list"),
    path("batches/<uuid:batch_id>/qr/", BatchQRCodeView.as_view(), name="batch-qr"),
    path("verify/<str:nafdac_number>/", DrugVerifyView.as_view(), name="drug-verify"),
]
