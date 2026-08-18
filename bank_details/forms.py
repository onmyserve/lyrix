from django import forms
from .models import BankDetail


class BankDetailForm(forms.ModelForm):
    class Meta:
        model = BankDetail
        fields = ['bank_name', 'ifsc_code', 'micr_code', 'branch_name']
        widgets = {
            'bank_name': forms.TextInput(attrs={
                'class': 'w-full bg-white border border-black/10 rounded-xl px-4 py-2.5 text-sm text-on-surface focus:outline-none focus:border-electric-violet focus:ring-1 focus:ring-electric-violet/30 transition-all',
                'placeholder': 'e.g. State Bank of India',
            }),
            'ifsc_code': forms.TextInput(attrs={
                'class': 'w-full bg-white border border-black/10 rounded-xl px-4 py-2.5 text-sm text-on-surface font-mono uppercase focus:outline-none focus:border-electric-violet focus:ring-1 focus:ring-electric-violet/30 transition-all',
                'placeholder': 'e.g. SBIN0001234',
            }),
            'micr_code': forms.TextInput(attrs={
                'class': 'w-full bg-white border border-black/10 rounded-xl px-4 py-2.5 text-sm text-on-surface font-mono focus:outline-none focus:border-electric-violet focus:ring-1 focus:ring-electric-violet/30 transition-all',
                'placeholder': 'e.g. 400002001',
            }),
            'branch_name': forms.TextInput(attrs={
                'class': 'w-full bg-white border border-black/10 rounded-xl px-4 py-2.5 text-sm text-on-surface focus:outline-none focus:border-electric-violet focus:ring-1 focus:ring-electric-violet/30 transition-all',
                'placeholder': 'e.g. Main Branch, Connaught Place',
            }),
        }

    def clean_ifsc_code(self):
        ifsc = self.cleaned_data.get('ifsc_code', '').strip().upper()
        if not ifsc:
            raise forms.ValidationError('IFSC code is required.')
        return ifsc
