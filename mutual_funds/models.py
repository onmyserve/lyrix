from django.db import models
from contacts.models import Contact


class MutualFund(models.Model):
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name='mutual_funds')
    name = models.CharField(max_length=200, blank=True, default='')
    mobile_no = models.CharField(max_length=20, blank=True, default='')
    pan = models.CharField(max_length=20, blank=True, default='')

    # SIP Register Fields
    sip_amt = models.CharField(max_length=50, blank=True, default='')
    sip_date = models.CharField(max_length=50, blank=True, default='')
    mode = models.CharField(max_length=50, blank=True, default='')
    sip_start_date = models.DateField(blank=True, null=True)
    sip_end_date = models.DateField(blank=True, null=True)
    bank = models.CharField(max_length=100, blank=True, default='')
    mandate_id = models.CharField(max_length=50, blank=True, default='')
    amc = models.CharField(max_length=100, blank=True, default='')
    fund_description = models.TextField(blank=True, default='')
    folio_number = models.CharField(max_length=50, blank=True, default='')

    # M F Register Fields
    transaction_date = models.DateField(blank=True, null=True)
    amount = models.CharField(max_length=50, blank=True, default='')
    stamp_duty = models.CharField(max_length=50, blank=True, default='')
    process_date = models.DateField(blank=True, null=True)
    price = models.CharField(max_length=50, blank=True, default='')
    units = models.CharField(max_length=50, blank=True, default='')
    remarks = models.TextField(blank=True, default='')
    transaction_description = models.TextField(blank=True, default='')
    transaction_id = models.CharField(max_length=100, blank=True, default='')

    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.contact:
            if not self.name:
                self.name = self.contact.name
            if not self.mobile_no:
                self.mobile_no = self.contact.mobile_no
            if not self.pan and hasattr(self.contact, 'pan_no'):
                self.pan = self.contact.pan_no
        super().save(*args, **kwargs)

    def __str__(self):
        disp_name = self.name or (self.contact.name if self.contact else f"Mutual Fund #{self.pk}")
        return f"{disp_name} - {self.amc or 'AMC'} ({self.sip_amt or 'SIP'})"
