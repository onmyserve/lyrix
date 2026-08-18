from django.contrib import admin
from .models import BankDetail


@admin.register(BankDetail)
class BankDetailAdmin(admin.ModelAdmin):
    list_display = ('bank_name', 'ifsc_code', 'micr_code', 'branch_name', 'created_at')
    search_fields = ('bank_name', 'ifsc_code', 'micr_code', 'branch_name')
    list_filter = ('bank_name', 'created_at')
