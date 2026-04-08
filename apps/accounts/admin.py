from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User, ManufacturerProfile

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    ordering = ["email"]
    list_display = ["email", "role", "company_name", "is_verified", "is_active", "dark_mode", "date_joined"]
    list_filter = ["role", "is_verified", "is_active", "is_staff", "date_joined"]
    search_fields = ["email", "company_name", "license_number"]
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Personal info"), {"fields": ("phone", "company_name", "license_number")}),
        (_("Role & Status"), {"fields": ("role", "is_verified", "dark_mode")}),
        (_("Permissions"), {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        (_("Important dates"), {"fields": ("last_login", "date_joined", "deleted_at")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "password1", "password2", "role"),
        }),
    )
    readonly_fields = ["date_joined", "last_login"]

@admin.register(ManufacturerProfile)
class ManufacturerProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "address"]
    search_fields = ["user__email", "user__company_name"]
