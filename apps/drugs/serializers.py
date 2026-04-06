from rest_framework import serializers
from .models import Drug, BatchNumber

class BatchNumberSerializer(serializers.ModelSerializer):
    is_expired = serializers.ReadOnlyField()
    class Meta:
        model = BatchNumber
        fields = ["id", "batch_number", "manufacture_date", "expiry_date", "quantity", "status", "is_expired", "created_at"]
        read_only_fields = ["id", "created_at"]

class DrugSerializer(serializers.ModelSerializer):
    batches = BatchNumberSerializer(many=True, read_only=True)
    manufacturer_name = serializers.CharField(source="manufacturer.company_name", read_only=True)
    class Meta:
        model = Drug
        fields = ["id", "name", "generic_name", "nafdac_number", "description", "dosage_form", "strength", "status", "manufacturer", "manufacturer_name", "batches", "created_at"]
        read_only_fields = ["id", "manufacturer", "created_at"]
    def create(self, validated_data):
        validated_data["manufacturer"] = self.context["request"].user
        return super().create(validated_data)
