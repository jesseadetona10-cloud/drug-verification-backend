from rest_framework import serializers
from .models import SupplyChainEvent

class SupplyChainEventSerializer(serializers.ModelSerializer):
    actor_email = serializers.CharField(source="actor.email", read_only=True)
    actor_company = serializers.CharField(source="actor.company_name", read_only=True)
    batch_number = serializers.CharField(source="batch.batch_number", read_only=True)
    drug_name = serializers.CharField(source="batch.drug.name", read_only=True)
    class Meta:
        model = SupplyChainEvent
        fields = ["id", "batch", "batch_number", "drug_name", "event_type", "actor", "actor_email", "actor_company", "location", "notes", "timestamp"]
        read_only_fields = ["id", "actor", "timestamp"]
    def create(self, validated_data):
        validated_data["actor"] = self.context["request"].user
        return super().create(validated_data)
