from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from rest_framework.throttling import ScopedRateThrottle
from apps.drugs.models import BatchNumber
from apps.alerts.models import Alert
from .models import VerificationLog
from .serializers import VerificationLogSerializer

class VerifyDrugView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "verify"

    def post(self, request):
        scanned_code = request.data.get("scanned_code")
        location = request.data.get("location", "")

        if not scanned_code:
            return Response({"detail": "scanned_code is required."}, status=status.HTTP_400_BAD_REQUEST)

        if len(scanned_code) > 500:
            return Response({"detail": "Invalid QR data."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            batch = BatchNumber.objects.get(batch_number=scanned_code)
            if batch.status == "recalled":
                result = "recalled"
            elif batch.is_expired:
                result = "expired"
            else:
                result = "authentic"
        except BatchNumber.DoesNotExist:
            batch = None
            result = "not_found"

        VerificationLog.objects.create(
            batch=batch,
            verified_by=request.user,
            scanned_code=scanned_code,
            result=result,
            location=location,
            ip_address=request.META.get("REMOTE_ADDR")
        )

        if result == "counterfeit" or result == "not_found":
            if batch:
                Alert.objects.create(
                    drug=batch.drug,
                    alert_type="counterfeit",
                    severity="critical",
                    title=f"Counterfeit detected: {batch.drug.name}",
                    message=f"Batch {scanned_code} flagged as {result} by {request.user.email} at {location}.",
                    created_by=request.user
                )

        return Response({
            "result": result,
            "scanned_code": scanned_code,
            "batch": batch.batch_number if batch else None,
            "drug_name": batch.drug.name if batch else None,
            "expiry_date": str(batch.expiry_date) if batch else None,
            "manufacturer": batch.drug.manufacturer.company_name if batch else None,
        })

class VerificationHistoryView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        logs = VerificationLog.objects.filter(verified_by=request.user).select_related("batch", "batch__drug")
        serializer = VerificationLogSerializer(logs, many=True)
        return Response(serializer.data)
