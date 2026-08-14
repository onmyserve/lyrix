from django.contrib import admin
from .models import MutualFund


@admin.register(MutualFund)
class MutualFundAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'mobile_no', 'pan', 'amc', 'sip_amt', 'sip_date', 'mode', 'created_at')
    search_fields = ('name', 'mobile_no', 'pan', 'amc', 'fund_description', 'folio_number', 'mandate_id', 'bank')
    list_filter = ('amc', 'mode', 'bank', 'created_at')
