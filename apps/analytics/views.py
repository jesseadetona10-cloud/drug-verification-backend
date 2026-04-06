from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from apps.drugs.models import Drug, BatchNumber
from apps.verification.models import VerificationLog
from apps.alerts.models import Alert
from apps.supply_chain.models import SupplyChainEvent
from django.db.models import Count

class DashboardStatsView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        user = request.user
        stats = {
            "total_drugs": Drug.objects.filter(manufacturer=user).count() if user.role == "manufacturer" else Drug.objects.count(),
            "total_batches": BatchNumber.objects.count(),
            "total_verifications": VerificationLog.objects.count(),
            "authentic_verifications": VerificationLog.objects.filter(result="authentic").count(),
            "counterfeit_verifications": VerificationLog.objects.filter(result="counterfeit").count(),
            "not_found_verifications": VerificationLog.objects.filter(result="not_found").count(),
            "total_alerts": Alert.objects.count(),
            "unresolved_alerts": Alert.objects.filter(is_resolved=False).count(),
            "total_supply_chain_events": SupplyChainEvent.objects.count(),
        }
        return Response(stats)

class VerificationStatsView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        stats = VerificationLog.objects.values("result").annotate(count=Count("result")).order_by("-count")
        return Response(list(stats))

class AlertStatsView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        by_type = Alert.objects.values("alert_type").annotate(count=Count("alert_type"))
        by_severity = Alert.objects.values("severity").annotate(count=Count("severity"))
        return Response({"by_type": list(by_type), "by_severity": list(by_severity)})
