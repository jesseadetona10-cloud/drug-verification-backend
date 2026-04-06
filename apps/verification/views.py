from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from apps.drugs.models import BatchNumber
from apps.common.qr_utils import verify_qr_code
from .models import VerificationLog
from .serializers import VerificationLogSerializer


class VerifyDrugView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        scanned_code = request.data.get('scanned_code')
        scanned_data = request.data.get('scanned_data')
        location = request.data.get('location', '')
        
        # Verify QR if provided
        if scanned_data:
            qr_verification = verify_qr_code(scanned_data)
            if not qr_verification['valid']:
                return Response({
                    'result': 'invalid_qr',
                    'detail': qr_verification.get('error', 'Invalid QR code')
                }, status=status.HTTP_400_BAD_REQUEST)
            scanned_code = qr_verification.get('batch_number', scanned_code)
        
        if not scanned_code:
            return Response({'detail': 'scanned_code is required.'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            batch = BatchNumber.objects.get(batch_number=scanned_code)
            if batch.status == 'recalled':
                result = 'recalled'
            elif batch.is_expired:
                result = 'expired'
            else:
                result = 'authentic'
        except BatchNumber.DoesNotExist:
            batch = None
            result = 'not_found'
        
        log = VerificationLog.objects.create(
            batch=batch,
            verified_by=request.user,
            scanned_code=scanned_code,
            result=result,
            location=location,
            ip_address=request.META.get('REMOTE_ADDR')
        )
        
        return Response({
            'result': result,
            'scanned_code': scanned_code,
            'batch': str(batch) if batch else None,
            'drug': batch.drug.name if batch else None,
            'verification_id': str(log.id)
        }, status=status.HTTP_200_OK)


class VerificationHistoryView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        logs = VerificationLog.objects.filter(verified_by=request.user)
        serializer = VerificationLogSerializer(logs, many=True)
        return Response(serializer.data)
