from django.urls import path
from .views import SupplyChainEventListCreateView, BatchSupplyChainView

urlpatterns = [
    path("events/", SupplyChainEventListCreateView.as_view(), name="supply-chain-events"),
    path("batch/<uuid:batch_id>/", BatchSupplyChainView.as_view(), name="batch-supply-chain"),
]
