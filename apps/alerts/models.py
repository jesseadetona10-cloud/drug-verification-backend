from django.db import models
from django.utils.translation import gettext_lazy as _
import uuid

class Alert(models.Model):
    class Severity(models.TextChoices):
        LOW = "low", _("Low")
        MEDIUM = "medium", _("Medium")
        HIGH = "high", _("High")
        CRITICAL = "critical", _("Critical")

    class AlertType(models.TextChoices):
        COUNTERFEIT = "counterfeit", _("Counterfeit Detected")
        RECALL = "recall", _("Drug Recall")
        EXPIRY = "expiry", _("Expiry Warning")
        SUSPICIOUS = "suspicious", _("Suspicious Activity")

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    drug = models.ForeignKey("drugs.Drug", on_delete=models.CASCADE, related_name="alerts", null=True, blank=True)
    alert_type = models.CharField(max_length=20, choices=AlertType.choices)
    severity = models.CharField(max_length=20, choices=Severity.choices, default=Severity.MEDIUM)
    title = models.CharField(max_length=255)
    message = models.TextField()
    is_resolved = models.BooleanField(default=False)
    created_by = models.ForeignKey("accounts.User", on_delete=models.SET_NULL, null=True, related_name="created_alerts")
    created_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "alerts"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.alert_type} - {self.title}"
