from rest_framework import generics, permissions, status, filters
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Drug, BatchNumber
from .serializers import DrugSerializer, BatchNumberSerializer
import qrcode
import base64
from io import BytesIO
import json

class IsManufacturer(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == "manufacturer"

class IsRegulator(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role in ["regulator", "admin"]

class DrugListCreateView(generics.ListCreateAPIView):
    serializer_class = DrugSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name", "generic_name", "nafdac_number"]
    ordering_fields = ["created_at", "name", "status"]
    ordering = ["-created_at"]

    def get_permissions(self):
        if self.request.method == "POST":
            return [permissions.IsAuthenticated(), IsManufacturer()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user
        if user.role == "manufacturer":
            return Drug.objects.filter(manufacturer=user)
        status_filter = self.request.query_params.get("status")
        queryset = Drug.objects.all()
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        return queryset

class DrugDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = DrugSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        user = self.request.user
        if user.role == "manufacturer":
            return Drug.objects.filter(manufacturer=user)
        return Drug.objects.all()

class DrugApproveView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsRegulator]
    def post(self, request, pk):
        try:
            drug = Drug.objects.get(pk=pk)
            drug.status = "active"
            drug.save()
            return Response({"detail": "Drug approved.", "id": str(drug.id)})
        except Drug.DoesNotExist:
            return Response({"detail": "Drug not found."}, status=status.HTTP_404_NOT_FOUND)

class DrugRejectView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsRegulator]
    def post(self, request, pk):
        try:
            drug = Drug.objects.get(pk=pk)
            drug.status = "rejected"
            drug.save()
            return Response({"detail": "Drug rejected.", "id": str(drug.id)})
        except Drug.DoesNotExist:
            return Response({"detail": "Drug not found."}, status=status.HTTP_404_NOT_FOUND)

class BatchListCreateView(generics.ListCreateAPIView):
    serializer_class = BatchNumberSerializer
    permission_classes = [permissions.IsAuthenticated, IsManufacturer]
    def get_queryset(self):
        return BatchNumber.objects.filter(drug__manufacturer=self.request.user)
    def perform_create(self, serializer):
        drug_id = self.kwargs["drug_id"]
        drug = Drug.objects.get(id=drug_id, manufacturer=self.request.user)
        serializer.save(drug=drug)

class BatchQRView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, batch_id):
        try:
            batch = BatchNumber.objects.get(id=batch_id)
        except BatchNumber.DoesNotExist:
            return Response({"detail": "Batch not found."}, status=status.HTTP_404_NOT_FOUND)

        qr_data = {
            "batch_number": batch.batch_number,
            "drug_name": batch.drug.name,
            "nafdac_number": batch.drug.nafdac_number,
            "manufacture_date": str(batch.manufacture_date),
            "expiry_date": str(batch.expiry_date),
            "manufacturer": batch.drug.manufacturer.company_name,
        }

        qr = qrcode.QRCode(version=1, box_size=10, border=4)
        qr.add_data(json.dumps(qr_data))
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0)
        img_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
        batch.qr_code_data = qr_data
        batch.save()

        return Response({
            "batch_number": batch.batch_number,
            "qr_image_base64": img_base64,
            "qr_data": qr_data,
        })

class DrugVerifyView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, nafdac_number):
        try:
            drug = Drug.objects.get(nafdac_number=nafdac_number)
            return Response(DrugSerializer(drug).data)
        except Drug.DoesNotExist:
            return Response({"detail": "Drug not found."}, status=status.HTTP_404_NOT_FOUND)
