with open('apps/supply_chain/urls.py', 'w') as f:
    f.write('from django.urls import path\n')
    f.write('from .views import SupplyChainEventListCreateView, BatchSupplyChainView\n\n')
    f.write('urlpatterns = [\n')
    f.write('    path("events/", SupplyChainEventListCreateView.as_view(), name="supply-chain-events"),\n')
    f.write('    path("batch/<uuid:batch_id>/", BatchSupplyChainView.as_view(), name="batch-supply-chain"),\n')
    f.write(']\n')
print('Done')
