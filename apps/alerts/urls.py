from django.urls import path
from .views import AlertListCreateView, AlertDetailView, ResolveAlertView
from .recall_views import RecallBatchView, BatchStatusView

urlpatterns = [
    path('', AlertListCreateView.as_view(), name='alert-list'),
    path('<uuid:pk>/', AlertDetailView.as_view(), name='alert-detail'),
    path('<uuid:pk>/resolve/', ResolveAlertView.as_view(), name='alert-resolve'),
    path('recall/<uuid:batch_id>/', RecallBatchView.as_view(), name='recall-batch'),
    path('status/<str:batch_number>/', BatchStatusView.as_view(), name='batch-status'),
]
