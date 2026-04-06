from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import SupplyChainEvent
from .serializers import SupplyChainEventSerializer

class SupplyChainEventListCreateView(generics.ListCreateAPIView):
    serializer_class = SupplyChainEventSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        user = self.request.user
        if user.role in ["regulator", "admin"]:
            return SupplyChainEvent.objects.all()
        return SupplyChainEvent.objects.filter(actor=user)

class BatchSupplyChainView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, batch_id):
        events = SupplyChainEvent.objects.filter(batch__id=batch_id).order_by("timestamp")
        serializer = SupplyChainEventSerializer(events, many=True)
        return Response(serializer.data)
