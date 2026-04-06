with open('apps/verification/serializers.py', 'w') as f:
    f.write('from rest_framework import serializers\n')
    f.write('from .models import VerificationLog\n\n')
    f.write('class VerificationLogSerializer(serializers.ModelSerializer):\n')
    f.write('    class Meta:\n')
    f.write('        model = VerificationLog\n')
    f.write('        fields = ["id", "scanned_code", "result", "location", "verified_at", "batch", "verified_by"]\n')
    f.write('        read_only_fields = ["id", "result", "verified_at", "verified_by"]\n')
print('Done')
