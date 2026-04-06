from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
import uuid
from .managers import UserManager

class User(AbstractBaseUser, PermissionsMixin):
    class Roles(models.TextChoices):
        MANUFACTURER = "manufacturer", _("Manufacturer")
        WHOLESALER = "wholesaler", _("Wholesaler")
        PHARMACIST = "pharmacist", _("Pharmacist")
        REGULATOR = "regulator", _("Regulator")
        PATIENT = "patient", _("Patient")

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(_("email address"), unique=True)
    phone = models.CharField(max_length=20, blank=True)
    role = models.CharField(max_length=20, choices=Roles.choices, default=Roles.PATIENT)
    company_name = models.CharField(max_length=200, blank=True)
    license_number = models.CharField(max_length=100, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        db_table = "users"
        ordering = ["-date_joined"]

    def __str__(self):
        return f"{self.email} ({self.role})"

    def soft_delete(self):
        self.deleted_at = timezone.now()
        self.is_active = False
        self.save()

    def restore(self):
        self.deleted_at = None
        self.is_active = True
        self.save()

class ManufacturerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="manufacturer_profile")
    registration_number = models.CharField(max_length=100, unique=True)
    address = models.TextField(blank=True)

    class Meta:
        db_table = "manufacturers"

    def __str__(self):
        return f"Manufacturer: {self.user.company_name}"
