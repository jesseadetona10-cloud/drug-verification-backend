from rest_framework import serializers
from .models import Alert

class AlertSerializer(serializers.ModelSerializer):
    created_by_email = serializers.CharField(source="created_by.email", read_only=True)
    drug_name = serializers.CharField(source="drug.name", read_only=True)
    class Meta:
        model = Alert
        fields = ["id", "drug", "drug_name", "alert_type", "severity", "title", "message", "is_resolved", "created_by", "created_by_email", "created_at", "resolved_at"]
        read_only_fields = ["id", "created_by", "created_at", "resolved_at"]
    def create(self, validated_data):
        validated_data["created_by"] = self.context["request"].user
        return super().create(validated_data)
