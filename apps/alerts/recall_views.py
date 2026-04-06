from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from apps.drugs.models import BatchNumber
from apps.common.permissions import IsRegulator, IsManufacturer


class RecallBatchView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, batch_id):
        user = request.user
        
        if user.role not in ['regulator', 'manufacturer']:
            return Response({'detail': 'Not authorized.'}, status=status.HTTP_403_FORBIDDEN)
        
        try:
            batch = BatchNumber.objects.get(id=batch_id)
            
            if user.role == 'manufacturer' and batch.drug.manufacturer != user:
                return Response({'detail': 'Not authorized.'}, status=status.HTTP_403_FORBIDDEN)
            
            batch.status = 'recalled'
            batch.save()
            
            return Response({
                'detail': 'Batch recalled successfully.',
                'batch_id': str(batch.id),
                'batch_number': batch.batch_number,
                'status': 'recalled'
            })
            
        except BatchNumber.DoesNotExist:
            return Response({'detail': 'Batch not found.'}, status=status.HTTP_404_NOT_FOUND)


class BatchStatusView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, batch_number):
        try:
            batch = BatchNumber.objects.get(batch_number=batch_number)
            return Response({
                'batch_number': batch.batch_number,
                'drug': batch.drug.name,
                'status': batch.status,
                'is_expired': batch.is_expired,
                'expiry_date': batch.expiry_date,
                'manufacturer': batch.drug.manufacturer.company_name
            })
        except BatchNumber.DoesNotExist:
            return Response({'detail': 'Batch not found.'}, status=status.HTTP_404_NOT_FOUND)
