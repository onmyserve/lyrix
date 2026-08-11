from django.db import models

class Contact(models.Model):
    name = models.CharField(max_length=200, blank=True, default='')
    mobile_no = models.CharField(max_length=20, blank=True, default='')
    dob = models.DateField(blank=True, null=True)
    email = models.EmailField(unique=True)
    place_of_birth = models.CharField(max_length=100, blank=True, default='')
    alternate_no = models.CharField(max_length=20, blank=True, default='')
    pan_no = models.CharField(max_length=20, blank=True, default='')
    pan_doc = models.FileField(upload_to='kyc_docs/pan/', blank=True, null=True)
    aadhar_no = models.CharField(max_length=20, blank=True, default='')
    aadhar_doc = models.FileField(upload_to='kyc_docs/aadhar/', blank=True, null=True)
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

    # Mandate Details
    bse_mandate_bank = models.CharField(max_length=100, blank=True, default='')
    bse_mandate_id = models.CharField(max_length=50, blank=True, default='')
    bse_mandate_limit = models.CharField(max_length=50, blank=True, default='')
    bse_mandate_payer = models.CharField(max_length=100, blank=True, default='')
    bse_mandate_umrn = models.CharField(max_length=50, blank=True, default='')
    cams_mandate_bank = models.CharField(max_length=100, blank=True, default='')
    cams_mandate_id = models.CharField(max_length=50, blank=True, default='')
    cams_mandate_limit = models.CharField(max_length=50, blank=True, default='')
    cams_mandate_payer = models.CharField(max_length=100, blank=True, default='')
    cams_mandate_umrn = models.CharField(max_length=50, blank=True, default='')
    kfin_mandate_bank = models.CharField(max_length=100, blank=True, default='')
    kfin_mandate_id = models.CharField(max_length=50, blank=True, default='')
    kfin_mandate_limit = models.CharField(max_length=50, blank=True, default='')
    kfin_mandate_payer = models.CharField(max_length=100, blank=True, default='')
    kfin_mandate_umrn = models.CharField(max_length=50, blank=True, default='')
    nse_mandate_bank = models.CharField(max_length=100, blank=True, default='')
    nse_mandate_id = models.CharField(max_length=50, blank=True, default='')
    nse_mandate_limit = models.CharField(max_length=50, blank=True, default='')
    nse_mandate_payer = models.CharField(max_length=100, blank=True, default='')
    nse_mandate_umrn = models.CharField(max_length=50, blank=True, default='')

    created_at = models.DateTimeField(auto_now_add=True)

    def sync_bank_accounts_to_legacy(self):
        savings_acc = self.bank_accounts.filter(account_type='Savings Account').first()
        if savings_acc:
            self.savings_bank_name = savings_acc.bank_name
            self.savings_account_no = savings_acc.account_no
            self.savings_ifsc_code = savings_acc.ifsc_code
            self.savings_micr_code = savings_acc.micr_code
            self.bank_name = savings_acc.bank_name
            self.account_no = savings_acc.account_no
            self.ifsc_code = savings_acc.ifsc_code
            self.micr_code = savings_acc.micr_code
            self.bank_account_type = 'Savings Account'
        
        current_acc = self.bank_accounts.filter(account_type='Current Account').first()
        if current_acc:
            self.current_bank_name = current_acc.bank_name
            self.current_account_no = current_acc.account_no
            self.current_ifsc_code = current_acc.ifsc_code
            self.current_micr_code = current_acc.micr_code
            if not savings_acc:
                self.bank_name = current_acc.bank_name
                self.account_no = current_acc.account_no
                self.ifsc_code = current_acc.ifsc_code
                self.micr_code = current_acc.micr_code
                self.bank_account_type = 'Current Account'
        
        self.save(update_fields=[
            'savings_bank_name', 'savings_account_no', 'savings_ifsc_code', 'savings_micr_code',
            'current_bank_name', 'current_account_no', 'current_ifsc_code', 'current_micr_code',
            'bank_name', 'account_no', 'ifsc_code', 'micr_code', 'bank_account_type'
        ])

    def sync_family_members_to_legacy(self):
        father = self.family_members.filter(relationship='Father').first()
        if father:
            self.father_name = father.name
            self.father_dob = father.dob
            self.father_mobile = father.mobile
            self.father_pan = father.pan
            self.father_aadhar = father.aadhar
            self.father_height_weight = father.height_weight

        mother = self.family_members.filter(relationship='Mother').first()
        if mother:
            self.mother_name = mother.name
            self.mother_dob = mother.dob
            self.mother_mobile = mother.mobile
            self.mother_pan = mother.pan
            self.mother_aadhar = mother.aadhar
            self.mother_height_weight = mother.height_weight

        spouse = self.family_members.filter(relationship='Spouse').first()
        if spouse:
            self.spouse_name = spouse.name
            self.spouse_dob = spouse.dob
            self.spouse_mobile = spouse.mobile
            self.spouse_pan = spouse.pan
            self.spouse_aadhar = spouse.aadhar
            self.spouse_height_weight = spouse.height_weight

        daughter = self.family_members.filter(relationship='Daughter').first()
        if daughter:
            self.daughter_name = daughter.name
            self.daughter_dob = daughter.dob
            self.daughter_mobile = daughter.mobile
            self.daughter_pan = daughter.pan
            self.daughter_aadhar = daughter.aadhar
            self.daughter_height_weight = daughter.height_weight

        son = self.family_members.filter(relationship='Son').first()
        if son:
            self.son_name = son.name
            self.son_dob = son.dob
            self.son_mobile = son.mobile
            self.son_pan = son.pan
            self.son_aadhar = son.aadhar
            self.son_height_weight = son.height_weight

        self.save(update_fields=[
            'father_name', 'father_dob', 'father_mobile', 'father_pan', 'father_aadhar', 'father_height_weight',
            'mother_name', 'mother_dob', 'mother_mobile', 'mother_pan', 'mother_aadhar', 'mother_height_weight',
            'spouse_name', 'spouse_dob', 'spouse_mobile', 'spouse_pan', 'spouse_aadhar', 'spouse_height_weight',
            'daughter_name', 'daughter_dob', 'daughter_mobile', 'daughter_pan', 'daughter_aadhar', 'daughter_height_weight',
            'son_name', 'son_dob', 'son_mobile', 'son_pan', 'son_aadhar', 'son_height_weight',
        ])

    def sync_nominees_to_legacy(self):
        primary_nominee = self.nominees.first()
        if primary_nominee:
            self.nominee_name = primary_nominee.name
            self.nominee_relationship = primary_nominee.relationship
            self.nominee_dob = primary_nominee.dob
            self.nominee_pan = primary_nominee.pan
            self.nominee_aadhar = primary_nominee.aadhar
            self.nominee_mobile = primary_nominee.mobile
            self.nominee_email = primary_nominee.email
            self.save(update_fields=[
                'nominee_name', 'nominee_relationship', 'nominee_dob',
                'nominee_pan', 'nominee_aadhar', 'nominee_mobile', 'nominee_email'
            ])

    def sync_mandates_to_legacy(self):
        bse_m = self.mandates.filter(provider__iexact='BSE').first()
        if bse_m:
            self.bse_mandate_bank = bse_m.bank_name
            self.bse_mandate_id = bse_m.mandate_id
            self.bse_mandate_limit = bse_m.mandate_limit
            self.bse_mandate_payer = bse_m.payer_name
            self.bse_mandate_umrn = bse_m.umrn

        cams_m = self.mandates.filter(provider__iexact='CAMS').first()
        if cams_m:
            self.cams_mandate_bank = cams_m.bank_name
            self.cams_mandate_id = cams_m.mandate_id
            self.cams_mandate_limit = cams_m.mandate_limit
            self.cams_mandate_payer = cams_m.payer_name
            self.cams_mandate_umrn = cams_m.umrn

        kfin_m = self.mandates.filter(provider__iexact='KFIN').first()
        if kfin_m:
            self.kfin_mandate_bank = kfin_m.bank_name
            self.kfin_mandate_id = kfin_m.mandate_id
            self.kfin_mandate_limit = kfin_m.mandate_limit
            self.kfin_mandate_payer = kfin_m.payer_name
            self.kfin_mandate_umrn = kfin_m.umrn

        nse_m = self.mandates.filter(provider__iexact='NSE').first()
        if nse_m:
            self.nse_mandate_bank = nse_m.bank_name
            self.nse_mandate_id = nse_m.mandate_id
            self.nse_mandate_limit = nse_m.mandate_limit
            self.nse_mandate_payer = nse_m.payer_name
            self.nse_mandate_umrn = nse_m.umrn

        self.save(update_fields=[
            'bse_mandate_bank', 'bse_mandate_id', 'bse_mandate_limit', 'bse_mandate_payer', 'bse_mandate_umrn',
            'cams_mandate_bank', 'cams_mandate_id', 'cams_mandate_limit', 'cams_mandate_payer', 'cams_mandate_umrn',
            'kfin_mandate_bank', 'kfin_mandate_id', 'kfin_mandate_limit', 'kfin_mandate_payer', 'kfin_mandate_umrn',
            'nse_mandate_bank', 'nse_mandate_id', 'nse_mandate_limit', 'nse_mandate_payer', 'nse_mandate_umrn',
        ])

    def save(self, *args, **kwargs):
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
        return self.name or f"Contact {self.pk}"


class BankAccount(models.Model):
    SAVINGS = 'Savings Account'
    CURRENT = 'Current Account'
    ACCOUNT_TYPE_CHOICES = [
        (SAVINGS, 'Savings Account'),
        (CURRENT, 'Current Account'),
    ]

    contact = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name='bank_accounts')
    account_type = models.CharField(max_length=50, choices=ACCOUNT_TYPE_CHOICES, default=SAVINGS)
    bank_name = models.CharField(max_length=100, blank=True, default='')
    account_no = models.CharField(max_length=50, blank=True, default='')
    ifsc_code = models.CharField(max_length=20, blank=True, default='')
    micr_code = models.CharField(max_length=20, blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.account_type} - {self.bank_name or 'Bank'} ({self.account_no})"


class FamilyMember(models.Model):
    RELATIONSHIP_CHOICES = [
        ('Father', 'Father'),
        ('Mother', 'Mother'),
        ('Spouse', 'Spouse'),
        ('Son', 'Son'),
        ('Daughter', 'Daughter'),
        ('Brother', 'Brother'),
        ('Sister', 'Sister'),
        ('Grandfather', 'Grandfather'),
        ('Grandmother', 'Grandmother'),
        ('Uncle', 'Uncle'),
        ('Aunt', 'Aunt'),
        ('Cousin', 'Cousin'),
        ('Guardian', 'Guardian'),
        ('Other', 'Other'),
    ]

    contact = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name='family_members')
    relationship = models.CharField(max_length=50, choices=RELATIONSHIP_CHOICES, default='Father')
    name = models.CharField(max_length=200, blank=True, default='')
    dob = models.DateField(blank=True, null=True)
    mobile = models.CharField(max_length=20, blank=True, default='')
    pan = models.CharField(max_length=20, blank=True, default='')
    pan_doc = models.FileField(upload_to='kyc_docs/family/pan/', blank=True, null=True)
    aadhar = models.CharField(max_length=20, blank=True, default='')
    aadhar_doc = models.FileField(upload_to='kyc_docs/family/aadhar/', blank=True, null=True)
    height_weight = models.CharField(max_length=50, blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.relationship} - {self.name or 'Member'}"


class Nominee(models.Model):
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name='nominees')
    name = models.CharField(max_length=200, blank=True, default='')
    relationship = models.CharField(max_length=100, blank=True, default='')
    dob = models.DateField(blank=True, null=True)
    pan = models.CharField(max_length=20, blank=True, default='')
    pan_doc = models.FileField(upload_to='kyc_docs/nominees/pan/', blank=True, null=True)
    aadhar = models.CharField(max_length=20, blank=True, default='')
    aadhar_doc = models.FileField(upload_to='kyc_docs/nominees/aadhar/', blank=True, null=True)
    mobile = models.CharField(max_length=20, blank=True, default='')
    email = models.EmailField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name or 'Nominee'} ({self.relationship or 'No Rel'})"


class Mandate(models.Model):
    PROVIDER_CHOICES = [
        ('BSE', 'BSE Mandate'),
        ('CAMS', 'CAMS Mandate'),
        ('KFIN', 'KFIN Mandate'),
        ('NSE', 'NSE Mandate'),
        ('Other', 'Other Mandate'),
    ]

    contact = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name='mandates')
    provider = models.CharField(max_length=50, choices=PROVIDER_CHOICES, default='BSE')
    bank_name = models.CharField(max_length=100, blank=True, default='')
    mandate_id = models.CharField(max_length=50, blank=True, default='')
    mandate_limit = models.CharField(max_length=50, blank=True, default='')
    payer_name = models.CharField(max_length=100, blank=True, default='')
    umrn = models.CharField(max_length=50, blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.provider} - {self.mandate_id or 'Mandate'} ({self.bank_name})"






