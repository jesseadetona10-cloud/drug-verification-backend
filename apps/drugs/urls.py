from django.urls import path
from .views import DrugListCreateView, DrugDetailView, BatchListCreateView, BatchQRView, DrugVerifyView, DrugApproveView, DrugRejectView

urlpatterns = [
    path("", DrugListCreateView.as_view(), name="drug-list"),
    path("<uuid:pk>/", DrugDetailView.as_view(), name="drug-detail"),
    path("<uuid:pk>/approve/", DrugApproveView.as_view(), name="drug-approve"),
    path("<uuid:pk>/reject/", DrugRejectView.as_view(), name="drug-reject"),
    path("<uuid:drug_id>/batches/", BatchListCreateView.as_view(), name="batch-list"),
    path("batches/<uuid:batch_id>/qr/", BatchQRView.as_view(), name="batch-qr"),
    path("verify/<str:nafdac_number>/", DrugVerifyView.as_view(), name="drug-verify"),
]
