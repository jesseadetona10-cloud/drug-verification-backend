from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils import timezone
from .models import Alert
from .serializers import AlertSerializer
from .notifications import send_counterfeit_alert_email, send_recall_alert_email

class AlertListCreateView(generics.ListCreateAPIView):
    serializer_class = AlertSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        queryset = Alert.objects.all()
        alert_type = self.request.query_params.get("type")
        severity = self.request.query_params.get("severity")
        if alert_type:
            queryset = queryset.filter(alert_type=alert_type)
        if severity:
            queryset = queryset.filter(severity=severity)
        return queryset
    def perform_create(self, serializer):
        alert = serializer.save()
        if alert.alert_type == "counterfeit":
            send_counterfeit_alert_email(alert)
        elif alert.alert_type == "recall":
            send_recall_alert_email(alert)

class AlertDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AlertSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Alert.objects.all()

class ResolveAlertView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request, pk):
        try:
            alert = Alert.objects.get(pk=pk)
            alert.is_resolved = True
            alert.resolved_at = timezone.now()
            alert.save()
            return Response({"detail": "Alert resolved.", "id": str(alert.id)})
        except Alert.DoesNotExist:
            return Response({"detail": "Alert not found."}, status=404)
