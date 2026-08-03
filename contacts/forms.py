from django import forms
from .models import Contact

INDIAN_DATE_INPUT_FORMATS = ['%d/%m/%Y', '%d-%m-%Y', '%Y-%m-%d']

class ContactForm(forms.ModelForm):
    mobile_no = forms.CharField(required=True, label="Mobile No")
    name = forms.CharField(required=True, label="Name")
    dob = forms.DateField(required=True, label="Date of Birth", input_formats=INDIAN_DATE_INPUT_FORMATS, widget=forms.DateInput(format='%d/%m/%Y', attrs={'type': 'text', 'placeholder': 'DD/MM/YYYY'}))
    email = forms.EmailField(required=True, label="Email")

    pan_no = forms.CharField(required=False, label="PAN")
    aadhar_no = forms.CharField(required=False, label="Aadhar")
    gst_no = forms.CharField(required=False, label="GST No")
    uin = forms.CharField(required=False, label="UIN")

    ckyc_no = forms.CharField(required=False, label="CKYC No")
    uiic_cid = forms.CharField(required=False, label="UIIC CID")
    tnia_cid = forms.CharField(required=False, label="TNIA CID")
    bse_ucc = forms.CharField(required=False, label="BSE UCC")
    nse_ucc = forms.CharField(required=False, label="NSE UCC")
    lic_cid = forms.CharField(required=False, label="LIC CID")

    pincode = forms.CharField(required=False, label="Pin Code")
    post_office = forms.CharField(required=False, label="Post Office")
    village = forms.CharField(required=False, label="Village")
    street_address = forms.CharField(required=False, label="Door No / Street")
    taluk = forms.CharField(required=False, label="Taluk")
    district = forms.CharField(required=False, label="District")
    state = forms.CharField(required=False, label="State")

    bank_account_type = forms.ChoiceField(
        required=False,
        label="Type",
        choices=[
            ('Savings Account', 'Savings Account'),
            ('Current Account', 'Current Account')
        ]
    )
    ifsc_code = forms.CharField(required=False, label="IFSC Code")
    micr_code = forms.CharField(required=False, label="MICR Code")
    bank_name = forms.CharField(required=False, label="Bank Name")
    account_no = forms.CharField(required=False, label="Account No")

    savings_bank_name = forms.CharField(required=False, label="Savings Bank Name")
    savings_account_no = forms.CharField(required=False, label="Savings Account No")
    savings_ifsc_code = forms.CharField(required=False, label="Savings IFSC Code")
    savings_micr_code = forms.CharField(required=False, label="Savings MICR Code")

    current_bank_name = forms.CharField(required=False, label="Current Bank Name")
    current_account_no = forms.CharField(required=False, label="Current Account No")
    current_ifsc_code = forms.CharField(required=False, label="Current IFSC Code")
    current_micr_code = forms.CharField(required=False, label="Current MICR Code")

    nominee_name = forms.CharField(required=False, label="Nominee Name")
    nominee_relationship = forms.CharField(required=False, label="Relationship")
    nominee_dob = forms.DateField(required=False, label="Nominee DOB", input_formats=INDIAN_DATE_INPUT_FORMATS, widget=forms.DateInput(format='%d/%m/%Y', attrs={'type': 'text', 'placeholder': 'DD/MM/YYYY'}))
    nominee_pan = forms.CharField(required=False, label="Nominee PAN")
    nominee_aadhar = forms.CharField(required=False, label="Nominee Aadhaar")
    nominee_mobile = forms.CharField(required=False, label="Nominee Mobile")
    nominee_email = forms.EmailField(required=False, label="Nominee Email")

    # Father
    father_name = forms.CharField(required=False, label="Father Name")
    father_dob = forms.DateField(required=False, label="Father DOB", input_formats=INDIAN_DATE_INPUT_FORMATS, widget=forms.DateInput(format='%d/%m/%Y', attrs={'type': 'text', 'placeholder': 'DD/MM/YYYY'}))
    father_mobile = forms.CharField(required=False, label="Father Mobile")
    father_pan = forms.CharField(required=False, label="Father PAN")
    father_aadhar = forms.CharField(required=False, label="Father Aadhaar")
    father_height_weight = forms.CharField(required=False, label="Father Height / Weight")

    # Mother
    mother_name = forms.CharField(required=False, label="Mother Name")
    mother_dob = forms.DateField(required=False, label="Mother DOB", input_formats=INDIAN_DATE_INPUT_FORMATS, widget=forms.DateInput(format='%d/%m/%Y', attrs={'type': 'text', 'placeholder': 'DD/MM/YYYY'}))
    mother_mobile = forms.CharField(required=False, label="Mother Mobile")
    mother_pan = forms.CharField(required=False, label="Mother PAN")
    mother_aadhar = forms.CharField(required=False, label="Mother Aadhaar")
    mother_height_weight = forms.CharField(required=False, label="Mother Height / Weight")

    # Spouse
    spouse_name = forms.CharField(required=False, label="Spouse Name")
    spouse_dob = forms.DateField(required=False, label="Spouse DOB", input_formats=INDIAN_DATE_INPUT_FORMATS, widget=forms.DateInput(format='%d/%m/%Y', attrs={'type': 'text', 'placeholder': 'DD/MM/YYYY'}))
    spouse_mobile = forms.CharField(required=False, label="Spouse Mobile")
    spouse_pan = forms.CharField(required=False, label="Spouse PAN")
    spouse_aadhar = forms.CharField(required=False, label="Spouse Aadhaar")
    spouse_height_weight = forms.CharField(required=False, label="Spouse Height / Weight")

    # Daughter
    daughter_name = forms.CharField(required=False, label="Daughter Name")
    daughter_dob = forms.DateField(required=False, label="Daughter DOB", input_formats=INDIAN_DATE_INPUT_FORMATS, widget=forms.DateInput(format='%d/%m/%Y', attrs={'type': 'text', 'placeholder': 'DD/MM/YYYY'}))
    daughter_mobile = forms.CharField(required=False, label="Daughter Mobile")
    daughter_pan = forms.CharField(required=False, label="Daughter PAN")
    daughter_aadhar = forms.CharField(required=False, label="Daughter Aadhaar")
    daughter_height_weight = forms.CharField(required=False, label="Daughter Height / Weight")

    # Son
    son_name = forms.CharField(required=False, label="Son Name")
    son_dob = forms.DateField(required=False, label="Son DOB", input_formats=INDIAN_DATE_INPUT_FORMATS, widget=forms.DateInput(format='%d/%m/%Y', attrs={'type': 'text', 'placeholder': 'DD/MM/YYYY'}))
    son_mobile = forms.CharField(required=False, label="Son Mobile")
    son_pan = forms.CharField(required=False, label="Son PAN")
    son_aadhar = forms.CharField(required=False, label="Son Aadhaar")
    
    class Meta:
        model = Contact
        fields = [
            'mobile_no', 'name', 'dob', 'email', 'place_of_birth', 'alternate_no',
            'pan_no', 'aadhar_no', 'gst_no', 'uin',
            'ckyc_no', 'uiic_cid', 'tnia_cid', 'bse_ucc', 'nse_ucc', 'lic_cid',
            'pincode', 'post_office', 'village', 'street_address', 'taluk', 'district', 'state',
            'bank_account_type', 'ifsc_code', 'micr_code', 'bank_name', 'account_no',
            'savings_bank_name', 'savings_account_no', 'savings_ifsc_code', 'savings_micr_code',
            'current_bank_name', 'current_account_no', 'current_ifsc_code', 'current_micr_code',
            'nominee_name', 'nominee_relationship', 'nominee_dob', 'nominee_pan',
            'nominee_aadhar', 'nominee_mobile', 'nominee_email',
            'father_name', 'father_dob', 'father_mobile', 'father_pan', 'father_aadhar', 'father_height_weight',
            'mother_name', 'mother_dob', 'mother_mobile', 'mother_pan', 'mother_aadhar', 'mother_height_weight',
            'spouse_name', 'spouse_dob', 'spouse_mobile', 'spouse_pan', 'spouse_aadhar', 'spouse_height_weight',
            'daughter_name', 'daughter_dob', 'daughter_mobile', 'daughter_pan', 'daughter_aadhar', 'daughter_height_weight',
            'son_name', 'son_dob', 'son_mobile', 'son_pan', 'son_aadhar', 'son_height_weight',
           
        ]










