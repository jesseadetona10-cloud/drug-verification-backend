from django.db import models
from django.utils.translation import gettext_lazy as _
import uuid

class VerificationLog(models.Model):
    class Result(models.TextChoices):
        AUTHENTIC = "authentic", _("Authentic")
        COUNTERFEIT = "counterfeit", _("Counterfeit")
        EXPIRED = "expired", _("Expired")
        RECALLED = "recalled", _("Recalled")
        NOT_FOUND = "not_found", _("Not Found")

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    batch = models.ForeignKey("drugs.BatchNumber", on_delete=models.SET_NULL, null=True, blank=True, related_name="verification_logs")
    verified_by = models.ForeignKey("accounts.User", on_delete=models.SET_NULL, null=True, blank=True, related_name="verifications")
    scanned_code = models.CharField(max_length=255)
    result = models.CharField(max_length=20, choices=Result.choices)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    location = models.CharField(max_length=255, blank=True)
    verified_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "verification_logs"
        ordering = ["-verified_at"]

    def __str__(self):
        return f"{self.scanned_code} - {self.result}"
