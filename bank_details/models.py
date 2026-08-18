from django.db import models


class BankDetail(models.Model):
    bank_name = models.CharField(max_length=200)
    ifsc_code = models.CharField(max_length=20, unique=True)
    micr_code = models.CharField(max_length=20, blank=True, default='')
    branch_name = models.CharField(max_length=200, blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.bank_name} ({self.ifsc_code})"
