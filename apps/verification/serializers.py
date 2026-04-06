from rest_framework import serializers
from .models import VerificationLog

class VerificationLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = VerificationLog
        fields = ["id", "scanned_code", "result", "location", "verified_at", "batch", "verified_by"]
        read_only_fields = ["id", "result", "verified_at", "verified_by"]
