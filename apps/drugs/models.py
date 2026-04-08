from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator
import uuid

nafdac_validator = RegexValidator(
    regex=r"^[A-Z][0-9]-[0-9]{4}$",
    message="NAFDAC number must follow format: A4-1234 (Letter + Number + dash + 4 digits)"
)

class Drug(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", _("Pending Approval")
        ACTIVE = "active", _("Active")
        REJECTED = "rejected", _("Rejected")
        RECALLED = "recalled", _("Recalled")
        EXPIRED = "expired", _("Expired")
        SUSPENDED = "suspended", _("Suspended")

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    generic_name = models.CharField(max_length=255, blank=True)
    manufacturer = models.ForeignKey("accounts.User", on_delete=models.CASCADE, related_name="drugs", limit_choices_to={"role": "manufacturer"})
    nafdac_number = models.CharField(max_length=100, unique=True, validators=[nafdac_validator])
    description = models.TextField(blank=True)
    dosage_form = models.CharField(max_length=100)
    strength = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    image = models.ImageField(upload_to="drugs/images/", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "drugs"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} ({self.nafdac_number})"


class BatchNumber(models.Model):
    class Status(models.TextChoices):
        ACTIVE = "active", _("Active")
        RECALLED = "recalled", _("Recalled")
        EXPIRED = "expired", _("Expired")

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    drug = models.ForeignKey(Drug, on_delete=models.CASCADE, related_name="batches")
    batch_number = models.CharField(max_length=100, unique=True)
    manufacture_date = models.DateField()
    expiry_date = models.DateField()
    quantity = models.PositiveIntegerField()
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ACTIVE)
    qr_code_data = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "batch_numbers"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.drug.name} - Batch {self.batch_number}"

    @property
    def is_expired(self):
        from django.utils import timezone
        return self.expiry_date < timezone.now().date()
