from django import forms
from contacts.models import Contact
from .models import MutualFund

INDIAN_DATE_INPUT_FORMATS = ['%d/%m/%Y', '%d-%m-%Y', '%Y-%m-%d']


class ContactChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        info_parts = [obj.name]
        if obj.mobile_no:
            info_parts.append(obj.mobile_no)
        if hasattr(obj, 'pan_no') and obj.pan_no:
            info_parts.append(f"PAN: {obj.pan_no}")
        return " - ".join(info_parts)


class MutualFundForm(forms.ModelForm):
    contact = ContactChoiceField(
        queryset=Contact.objects.all().order_by('name'),
        required=True,
        label="Select Member / Contact",
        empty_label="-- Select a Contact from Members --",
        widget=forms.Select(attrs={
            'class': 'w-full bg-white border border-black/10 focus:border-electric-violet focus:ring-1 focus:ring-electric-violet/30 rounded-xl py-3 px-4 text-on-surface shadow-sm transition-all',
            'id': 'contact-select'
        })
    )
    name = forms.CharField(
        required=False,
        label="Name",
        widget=forms.TextInput(attrs={
            'class': 'w-full bg-white border border-black/10 focus:border-electric-violet focus:ring-1 focus:ring-electric-violet/30 rounded-xl py-3 px-4 text-on-surface placeholder:text-outline shadow-sm transition-all bg-surface-variant/10',
            'placeholder': 'Auto-filled from selected contact',
            'id': 'name-input'
        })
    )
    mobile_no = forms.CharField(
        required=False,
        label="Mobile Number",
        widget=forms.TextInput(attrs={
            'class': 'w-full bg-white border border-black/10 focus:border-electric-violet focus:ring-1 focus:ring-electric-violet/30 rounded-xl py-3 px-4 text-on-surface placeholder:text-outline shadow-sm transition-all bg-surface-variant/10',
            'placeholder': 'Auto-filled from selected contact',
            'id': 'mobile-input'
        })
    )
    pan = forms.CharField(
        required=False,
        label="PAN Number",
        widget=forms.TextInput(attrs={
            'class': 'w-full bg-white border border-black/10 focus:border-electric-violet focus:ring-1 focus:ring-electric-violet/30 rounded-xl py-3 px-4 text-on-surface placeholder:text-outline shadow-sm transition-all bg-surface-variant/10',
            'placeholder': 'Auto-filled from selected contact',
            'id': 'pan-input'
        })
    )

    # SIP Register Fields
    sip_amt = forms.CharField(
        required=False,
        label="SIP Amount",
        widget=forms.TextInput(attrs={
            'class': 'w-full bg-white border border-black/10 focus:border-electric-violet focus:ring-1 focus:ring-electric-violet/30 rounded-xl py-3 px-4 text-on-surface placeholder:text-outline shadow-sm transition-all',
            'placeholder': 'e.g. 5000'
        })
    )
    sip_date = forms.CharField(
        required=False,
        label="SIP Date",
        widget=forms.TextInput(attrs={
            'class': 'w-full bg-white border border-black/10 focus:border-electric-violet focus:ring-1 focus:ring-electric-violet/30 rounded-xl py-3 px-4 text-on-surface placeholder:text-outline shadow-sm transition-all',
            'placeholder': 'e.g. 5th / 10th / 15th'
        })
    )
    mode = forms.CharField(
        required=False,
        label="Mode",
        widget=forms.TextInput(attrs={
            'class': 'w-full bg-white border border-black/10 focus:border-electric-violet focus:ring-1 focus:ring-electric-violet/30 rounded-xl py-3 px-4 text-on-surface placeholder:text-outline shadow-sm transition-all',
            'placeholder': 'e.g. Monthly / E-Mandate / Physical'
        })
    )
    sip_start_date = forms.DateField(
        required=False,
        label="SIP Start Date",
        input_formats=INDIAN_DATE_INPUT_FORMATS,
        widget=forms.DateInput(format='%d/%m/%Y', attrs={
            'class': 'date-input w-full bg-white border border-black/10 focus:border-electric-violet focus:ring-1 focus:ring-electric-violet/30 rounded-xl py-3 px-4 text-on-surface placeholder:text-outline shadow-sm transition-all',
            'placeholder': 'DD/MM/YYYY'
        })
    )
    sip_end_date = forms.DateField(
        required=False,
        label="SIP End Date",
        input_formats=INDIAN_DATE_INPUT_FORMATS,
        widget=forms.DateInput(format='%d/%m/%Y', attrs={
            'class': 'date-input w-full bg-white border border-black/10 focus:border-electric-violet focus:ring-1 focus:ring-electric-violet/30 rounded-xl py-3 px-4 text-on-surface placeholder:text-outline shadow-sm transition-all',
            'placeholder': 'DD/MM/YYYY'
        })
    )
    bank = forms.CharField(
        required=False,
        label="Bank Name",
        widget=forms.TextInput(attrs={
            'class': 'w-full bg-white border border-black/10 focus:border-electric-violet focus:ring-1 focus:ring-electric-violet/30 rounded-xl py-3 px-4 text-on-surface placeholder:text-outline shadow-sm transition-all',
            'placeholder': 'e.g. HDFC Bank'
        })
    )
    mandate_id = forms.CharField(
        required=False,
        label="Mandate ID",
        widget=forms.TextInput(attrs={
            'class': 'w-full bg-white border border-black/10 focus:border-electric-violet focus:ring-1 focus:ring-electric-violet/30 rounded-xl py-3 px-4 text-on-surface placeholder:text-outline shadow-sm transition-all',
            'placeholder': 'e.g. MANDATE12345'
        })
    )
    amc = forms.CharField(
        required=False,
        label="AMC Name",
        widget=forms.TextInput(attrs={
            'class': 'w-full bg-white border border-black/10 focus:border-electric-violet focus:ring-1 focus:ring-electric-violet/30 rounded-xl py-3 px-4 text-on-surface placeholder:text-outline shadow-sm transition-all',
            'placeholder': 'e.g. HDFC Mutual Fund'
        })
    )
    fund_description = forms.CharField(
        required=False,
        label="Fund Description",
        widget=forms.Textarea(attrs={
            'rows': 3,
            'class': 'w-full bg-white border border-black/10 focus:border-electric-violet focus:ring-1 focus:ring-electric-violet/30 rounded-xl py-3 px-4 text-on-surface placeholder:text-outline shadow-sm transition-all',
            'placeholder': 'e.g. HDFC Top 100 Fund Direct Plan Growth'
        })
    )
    folio_number = forms.CharField(
        required=False,
        label="Folio Number",
        widget=forms.TextInput(attrs={
            'class': 'w-full bg-white border border-black/10 focus:border-electric-violet focus:ring-1 focus:ring-electric-violet/30 rounded-xl py-3 px-4 text-on-surface placeholder:text-outline shadow-sm transition-all',
            'placeholder': 'e.g. 91029384/11'
        })
    )

    # M F Register Fields
    transaction_date = forms.DateField(
        required=False,
        label="Transaction Date",
        input_formats=INDIAN_DATE_INPUT_FORMATS,
        widget=forms.DateInput(format='%d/%m/%Y', attrs={
            'class': 'date-input w-full bg-white border border-black/10 focus:border-electric-violet focus:ring-1 focus:ring-electric-violet/30 rounded-xl py-3 px-4 text-on-surface placeholder:text-outline shadow-sm transition-all',
            'placeholder': 'DD/MM/YYYY'
        })
    )
    amount = forms.CharField(
        required=False,
        label="Amount",
        widget=forms.TextInput(attrs={
            'class': 'w-full bg-white border border-black/10 focus:border-electric-violet focus:ring-1 focus:ring-electric-violet/30 rounded-xl py-3 px-4 text-on-surface placeholder:text-outline shadow-sm transition-all',
            'placeholder': 'e.g. ₹ 10,000'
        })
    )
    stamp_duty = forms.CharField(
        required=False,
        label="Stamp Duty",
        widget=forms.TextInput(attrs={
            'class': 'w-full bg-white border border-black/10 focus:border-electric-violet focus:ring-1 focus:ring-electric-violet/30 rounded-xl py-3 px-4 text-on-surface placeholder:text-outline shadow-sm transition-all',
            'placeholder': 'e.g. 0.50'
        })
    )
    process_date = forms.DateField(
        required=False,
        label="Process Date",
        input_formats=INDIAN_DATE_INPUT_FORMATS,
        widget=forms.DateInput(format='%d/%m/%Y', attrs={
            'class': 'date-input w-full bg-white border border-black/10 focus:border-electric-violet focus:ring-1 focus:ring-electric-violet/30 rounded-xl py-3 px-4 text-on-surface placeholder:text-outline shadow-sm transition-all',
            'placeholder': 'DD/MM/YYYY'
        })
    )
    price = forms.CharField(
        required=False,
        label="Price (NAV)",
        widget=forms.TextInput(attrs={
            'class': 'w-full bg-white border border-black/10 focus:border-electric-violet focus:ring-1 focus:ring-electric-violet/30 rounded-xl py-3 px-4 text-on-surface placeholder:text-outline shadow-sm transition-all',
            'placeholder': 'e.g. 142.50'
        })
    )
    units = forms.CharField(
        required=False,
        label="Units",
        widget=forms.TextInput(attrs={
            'class': 'w-full bg-white border border-black/10 focus:border-electric-violet focus:ring-1 focus:ring-electric-violet/30 rounded-xl py-3 px-4 text-on-surface placeholder:text-outline shadow-sm transition-all',
            'placeholder': 'e.g. 70.175'
        })
    )
    remarks = forms.CharField(
        required=False,
        label="Remarks",
        widget=forms.Textarea(attrs={
            'rows': 2,
            'class': 'w-full bg-white border border-black/10 focus:border-electric-violet focus:ring-1 focus:ring-electric-violet/30 rounded-xl py-3 px-4 text-on-surface placeholder:text-outline shadow-sm transition-all',
            'placeholder': 'Additional remarks...'
        })
    )
    transaction_description = forms.CharField(
        required=False,
        label="Transaction Description",
        widget=forms.Textarea(attrs={
            'rows': 2,
            'class': 'w-full bg-white border border-black/10 focus:border-electric-violet focus:ring-1 focus:ring-electric-violet/30 rounded-xl py-3 px-4 text-on-surface placeholder:text-outline shadow-sm transition-all',
            'placeholder': 'Transaction details or description...'
        })
    )
    transaction_id = forms.CharField(
        required=False,
        label="Transaction ID",
        widget=forms.TextInput(attrs={
            'class': 'w-full bg-white border border-black/10 focus:border-electric-violet focus:ring-1 focus:ring-electric-violet/30 rounded-xl py-3 px-4 text-on-surface placeholder:text-outline shadow-sm transition-all',
            'placeholder': 'e.g. TXN987654321'
        })
    )

    class Meta:
        model = MutualFund
        fields = [
            'contact', 'name', 'mobile_no', 'pan', 'sip_amt', 'sip_date',
            'mode', 'sip_start_date', 'sip_end_date', 'bank', 'mandate_id',
            'amc', 'fund_description', 'folio_number',
            'transaction_date', 'amount', 'stamp_duty', 'process_date',
            'price', 'units', 'remarks', 'transaction_description', 'transaction_id'
        ]

    def clean(self):
        cleaned_data = super().clean()
        contact = cleaned_data.get('contact')
        name = cleaned_data.get('name')
        mobile_no = cleaned_data.get('mobile_no')
        pan = cleaned_data.get('pan')

        if contact:
            if not name:
                cleaned_data['name'] = contact.name
            if not mobile_no:
                cleaned_data['mobile_no'] = contact.mobile_no
            if not pan and hasattr(contact, 'pan_no'):
                cleaned_data['pan'] = contact.pan_no

        return cleaned_data
