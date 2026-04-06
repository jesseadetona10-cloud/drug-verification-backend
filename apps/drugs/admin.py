from django.contrib import admin
from .models import Drug, BatchNumber


@admin.register(Drug)
class DrugAdmin(admin.ModelAdmin):
    list_display = ['name', 'nafdac_number', 'manufacturer', 'status', 'created_at']
    list_filter = ['status', 'dosage_form']
    search_fields = ['name', 'nafdac_number', 'generic_name']


@admin.register(BatchNumber)
class BatchNumberAdmin(admin.ModelAdmin):
    list_display = ['drug', 'batch_number', 'expiry_date', 'status']
    list_filter = ['status']
    search_fields = ['batch_number', 'drug__name']
