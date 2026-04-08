from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from apps.drugs.models import BatchNumber
from apps.alerts.models import Alert

class Command(BaseCommand):
    help = "Check for batches expiring within 30 days and create alerts"

    def handle(self, *args, **kwargs):
        thirty_days = timezone.now().date() + timedelta(days=30)
        expiring = BatchNumber.objects.filter(
            expiry_date__lte=thirty_days,
            expiry_date__gte=timezone.now().date(),
            status="active"
        )
        count = 0
        for batch in expiring:
            exists = Alert.objects.filter(
                drug=batch.drug,
                alert_type="expiry",
                is_resolved=False
            ).exists()
            if not exists:
                Alert.objects.create(
                    drug=batch.drug,
                    alert_type="expiry",
                    severity="high",
                    title=f"Expiry Warning: {batch.drug.name}",
                    message=f"Batch {batch.batch_number} expires on {batch.expiry_date}. Please take action.",
                    created_by=None
                )
                count += 1
        self.stdout.write(f"Created {count} expiry alerts.")
