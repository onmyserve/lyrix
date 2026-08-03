from django.db import models

class Contact(models.Model):
    first_name = models.CharField(max_length=100, blank=True, default='')
    last_name = models.CharField(max_length=100, blank=True, default='')
    name = models.CharField(max_length=200, blank=True, default='')
    mobile_no = models.CharField(max_length=20, blank=True, default='')
    dob = models.DateField(blank=True, null=True)
    email = models.EmailField(unique=True)
    place_of_birth = models.CharField(max_length=100, blank=True, default='')
    alternate_no = models.CharField(max_length=20, blank=True, default='')
    pan_no = models.CharField(max_length=20, blank=True, default='')
    aadhar_no = models.CharField(max_length=20, blank=True, default='')
    gst_no = models.CharField(max_length=25, blank=True, default='')
    uin = models.CharField(max_length=30, blank=True, default='')
    ckyc_no = models.CharField(max_length=30, blank=True, default='')
    uiic_cid = models.CharField(max_length=30, blank=True, default='')
    tnia_cid = models.CharField(max_length=30, blank=True, default='')
    bse_ucc = models.CharField(max_length=30, blank=True, default='')
    nse_ucc = models.CharField(max_length=30, blank=True, default='')
    lic_cid = models.CharField(max_length=30, blank=True, default='')
    pincode = models.CharField(max_length=15, blank=True, default='')
    post_office = models.CharField(max_length=100, blank=True, default='')
    village = models.CharField(max_length=100, blank=True, default='')
    street_address = models.CharField(max_length=255, blank=True, default='')
    taluk = models.CharField(max_length=100, blank=True, default='')
    district = models.CharField(max_length=100, blank=True, default='')
    state = models.CharField(max_length=100, blank=True, default='')
    bank_account_type = models.CharField(max_length=50, blank=True, default='Savings Account')
    ifsc_code = models.CharField(max_length=20, blank=True, default='')
    micr_code = models.CharField(max_length=20, blank=True, default='')
    bank_name = models.CharField(max_length=100, blank=True, default='')
    account_no = models.CharField(max_length=50, blank=True, default='')
    savings_bank_name = models.CharField(max_length=100, blank=True, default='')
    savings_account_no = models.CharField(max_length=50, blank=True, default='')
    savings_ifsc_code = models.CharField(max_length=20, blank=True, default='')
    savings_micr_code = models.CharField(max_length=20, blank=True, default='')
    current_bank_name = models.CharField(max_length=100, blank=True, default='')
    current_account_no = models.CharField(max_length=50, blank=True, default='')
    current_ifsc_code = models.CharField(max_length=20, blank=True, default='')
    current_micr_code = models.CharField(max_length=20, blank=True, default='')
    nominee_name = models.CharField(max_length=200, blank=True, default='')
    nominee_relationship = models.CharField(max_length=100, blank=True, default='')
    nominee_dob = models.DateField(blank=True, null=True)
    nominee_pan = models.CharField(max_length=20, blank=True, default='')
    nominee_aadhar = models.CharField(max_length=20, blank=True, default='')
    nominee_mobile = models.CharField(max_length=20, blank=True, default='')
    nominee_email = models.EmailField(blank=True, default='')

    # Father Details
    father_name = models.CharField(max_length=200, blank=True, default='')
    father_dob = models.DateField(blank=True, null=True)
    father_mobile = models.CharField(max_length=20, blank=True, default='')
    father_pan = models.CharField(max_length=20, blank=True, default='')
    father_aadhar = models.CharField(max_length=20, blank=True, default='')
    father_height_weight = models.CharField(max_length=50, blank=True, default='')

    # Mother Details
    mother_name = models.CharField(max_length=200, blank=True, default='')
    mother_dob = models.DateField(blank=True, null=True)
    mother_mobile = models.CharField(max_length=20, blank=True, default='')
    mother_pan = models.CharField(max_length=20, blank=True, default='')
    mother_aadhar = models.CharField(max_length=20, blank=True, default='')
    mother_height_weight = models.CharField(max_length=50, blank=True, default='')

    # Spouse Details
    spouse_name = models.CharField(max_length=200, blank=True, default='')
    spouse_dob = models.DateField(blank=True, null=True)
    spouse_mobile = models.CharField(max_length=20, blank=True, default='')
    spouse_pan = models.CharField(max_length=20, blank=True, default='')
    spouse_aadhar = models.CharField(max_length=20, blank=True, default='')
    spouse_height_weight = models.CharField(max_length=50, blank=True, default='')

    # Daughter Details
    daughter_name = models.CharField(max_length=200, blank=True, default='')
    daughter_dob = models.DateField(blank=True, null=True)
    daughter_mobile = models.CharField(max_length=20, blank=True, default='')
    daughter_pan = models.CharField(max_length=20, blank=True, default='')
    daughter_aadhar = models.CharField(max_length=20, blank=True, default='')
    daughter_height_weight = models.CharField(max_length=50, blank=True, default='')

    # Son Details
    son_name = models.CharField(max_length=200, blank=True, default='')
    son_dob = models.DateField(blank=True, null=True)
    son_mobile = models.CharField(max_length=20, blank=True, default='')
    son_pan = models.CharField(max_length=20, blank=True, default='')
    son_aadhar = models.CharField(max_length=20, blank=True, default='')
    son_height_weight = models.CharField(max_length=50, blank=True, default='')

    # Mandate Details (NSE, BSE, CAMS, KFIN)
    nse_mandate_payer = models.CharField(max_length=100, blank=True, default='')
    nse_mandate_id = models.CharField(max_length=50, blank=True, default='')
    nse_mandate_umrn = models.CharField(max_length=50, blank=True, default='')
    nse_mandate_limit = models.CharField(max_length=50, blank=True, default='')
    nse_mandate_bank = models.CharField(max_length=100, blank=True, default='')

    bse_mandate_payer = models.CharField(max_length=100, blank=True, default='')
    bse_mandate_id = models.CharField(max_length=50, blank=True, default='')
    bse_mandate_umrn = models.CharField(max_length=50, blank=True, default='')
    bse_mandate_limit = models.CharField(max_length=50, blank=True, default='')
    bse_mandate_bank = models.CharField(max_length=100, blank=True, default='')

    cams_mandate_payer = models.CharField(max_length=100, blank=True, default='')
    cams_mandate_id = models.CharField(max_length=50, blank=True, default='')
    cams_mandate_umrn = models.CharField(max_length=50, blank=True, default='')
    cams_mandate_limit = models.CharField(max_length=50, blank=True, default='')
    cams_mandate_bank = models.CharField(max_length=100, blank=True, default='')

    kfin_mandate_payer = models.CharField(max_length=100, blank=True, default='')
    kfin_mandate_id = models.CharField(max_length=50, blank=True, default='')
    kfin_mandate_umrn = models.CharField(max_length=50, blank=True, default='')
    kfin_mandate_limit = models.CharField(max_length=50, blank=True, default='')
    kfin_mandate_bank = models.CharField(max_length=100, blank=True, default='')

    tag = models.CharField(max_length=50, default="Customer")
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.name and not (self.first_name or self.last_name):
            parts = self.name.strip().split(' ', 1)
            self.first_name = parts[0]
            self.last_name = parts[1] if len(parts) > 1 else ''
        elif (self.first_name or self.last_name) and not self.name:
            self.name = f"{self.first_name} {self.last_name}".strip()
        if not self.bank_name and self.savings_bank_name:
            self.bank_name = self.savings_bank_name
        if not self.account_no and self.savings_account_no:
            self.account_no = self.savings_account_no
        if not self.ifsc_code and self.savings_ifsc_code:
            self.ifsc_code = self.savings_ifsc_code
        if not self.micr_code and self.savings_micr_code:
            self.micr_code = self.savings_micr_code
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name or f"{self.first_name} {self.last_name}".strip() or f"Contact {self.pk}"


