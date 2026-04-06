from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Drug, BatchNumber
from .serializers import DrugSerializer, BatchNumberSerializer
from apps.common.permissions import IsManufacturer
from apps.common.qr_utils import generate_batch_qr

class DrugListCreateView(generics.ListCreateAPIView):
    serializer_class = DrugSerializer
    def get_permissions(self):
        if self.request.method == "POST":
            return [permissions.IsAuthenticated(), IsManufacturer()]
        return [permissions.IsAuthenticated()]
    def get_queryset(self):
        user = self.request.user
        if user.role == "manufacturer":
            return Drug.objects.filter(manufacturer=user)
        return Drug.objects.all()

class DrugDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = DrugSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        user = self.request.user
        if user.role == "manufacturer":
            return Drug.objects.filter(manufacturer=user)
        return Drug.objects.all()

class BatchListCreateView(generics.ListCreateAPIView):
    serializer_class = BatchNumberSerializer
    permission_classes = [permissions.IsAuthenticated, IsManufacturer]
    def get_queryset(self):
        return BatchNumber.objects.filter(drug__manufacturer=self.request.user)
    def perform_create(self, serializer):
        drug_id = self.kwargs["drug_id"]
        drug = Drug.objects.get(id=drug_id, manufacturer=self.request.user)
        batch = serializer.save(drug=drug)
        qr_data = generate_batch_qr(batch_number=batch.batch_number, drug_id=drug.id, manufacturer_id=self.request.user.id)
        batch.qr_code_data = qr_data["qr_data"]
        batch.save()

class BatchQRCodeView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsManufacturer]
    def get(self, request, batch_id):
        try:
            batch = BatchNumber.objects.get(id=batch_id, drug__manufacturer=request.user)
            qr_result = generate_batch_qr(batch_number=batch.batch_number, drug_id=batch.drug.id, manufacturer_id=request.user.id)
            return Response({"batch_id": str(batch.id), "batch_number": batch.batch_number, "qr_data": qr_result["qr_data"], "qr_image_base64": qr_result["qr_image_base64"]})
        except BatchNumber.DoesNotExist:
            return Response({"detail": "Batch not found."}, status=status.HTTP_404_NOT_FOUND)

class DrugVerifyView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, nafdac_number):
        try:
            drug = Drug.objects.get(nafdac_number=nafdac_number)
            return Response(DrugSerializer(drug).data)
        except Drug.DoesNotExist:
            return Response({"detail": "Drug not found."}, status=status.HTTP_404_NOT_FOUND)


class ApproveDrugView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request, pk):
        if request.user.role != "regulator":
            return Response({"detail": "Only regulators can approve drugs."}, status=status.HTTP_403_FORBIDDEN)
        try:
            drug = Drug.objects.get(pk=pk)
            drug.status = "active"
            drug.save()
            return Response({"detail": "Drug approved successfully."})
        except Drug.DoesNotExist:
            return Response({"detail": "Drug not found."}, status=status.HTTP_404_NOT_FOUND)

class RejectDrugView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request, pk):
        if request.user.role != "regulator":
            return Response({"detail": "Only regulators can reject drugs."}, status=status.HTTP_403_FORBIDDEN)
        try:
            drug = Drug.objects.get(pk=pk)
            drug.status = "rejected"
            drug.save()
            return Response({"detail": "Drug rejected."})
        except Drug.DoesNotExist:
            return Response({"detail": "Drug not found."}, status=status.HTTP_404_NOT_FOUND)

class PendingDrugsView(generics.ListAPIView):
    serializer_class = DrugSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        if self.request.user.role != "regulator":
            return Drug.objects.none()
        return Drug.objects.filter(status="pending")
