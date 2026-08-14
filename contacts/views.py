from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Contact, BankAccount, FamilyMember, Nominee, Mandate
from .forms import ContactForm, BankAccountFormSet, FamilyMemberFormSet, NomineeFormSet, MandateFormSet
from utils.search import ModelSearcher
from utils.importer import ModelFileImporter
from utils.exporter import ModelFileExporter
from utils.filters import ModelFilterer

contact_searcher = ModelSearcher(
    search_fields=['name', 'email', 'mobile_no'],
    param_name='q'
)

contact_filterer = ModelFilterer(
    exact_fields=['state', 'district', 'bank_account_type'],
    date_fields=['created_at']
)

contact_importer = ModelFileImporter(
    model_class=Contact,
    field_mapping={
        'name': ['name', 'full_name', 'full name', 'first_name', 'last_name', 'contact name'],
        'email': ['email', 'email address', 'e-mail', 'mail'],
        'mobile_no': ['mobile_no', 'mobile', 'phone', 'mobile no'],
    },
    required_fields=['name', 'email'],
    unique_key='email',
    update_existing=True,
    default_values={}
)

contact_exporter = ModelFileExporter(
    model_class=Contact,
    header_labels={
        'id': 'ID',
        'name': 'Name',
        'mobile_no': 'Mobile No',
        'dob': 'Date of Birth',
        'email': 'Email Address',
        'place_of_birth': 'Place of Birth',
        'alternate_no': 'Alternate No',
        'pan_no': 'PAN No',
        'aadhar_no': 'Aadhar No',
        'gst_no': 'GST No',
        'uin': 'UIN',
        'ckyc_no': 'CKYC No',
        'uiic_cid': 'UIIC CID',
        'tnia_cid': 'TNIA CID',
        'bse_ucc': 'BSE UCC',
        'nse_ucc': 'NSE UCC',
        'lic_cid': 'LIC CID',
        'pincode': 'Pincode',
        'post_office': 'Post Office',
        'village': 'Village',
        'street_address': 'Street Address',
        'taluk': 'Taluk',
        'district': 'District',
        'state': 'State',
        'bank_account_type': 'Bank Account Type',
        'ifsc_code': 'IFSC Code',
        'micr_code': 'MICR Code',
        'bank_name': 'Bank Name',
        'account_no': 'Account No',
        'savings_bank_name': 'Savings Bank Name',
        'savings_account_no': 'Savings Account No',
        'savings_ifsc_code': 'Savings IFSC Code',
        'savings_micr_code': 'Savings MICR Code',
        'current_bank_name': 'Current Bank Name',
        'current_account_no': 'Current Account No',
        'current_ifsc_code': 'Current IFSC Code',
        'current_micr_code': 'Current MICR Code',
        'nominee_name': 'Nominee Name',
        'nominee_relationship': 'Nominee Relationship',
        'nominee_dob': 'Nominee Date of Birth',
        'nominee_pan': 'Nominee PAN',
        'nominee_aadhar': 'Nominee Aadhar',
        'nominee_mobile': 'Nominee Mobile',
        'nominee_email': 'Nominee Email',
        'father_name': 'Father Name',
        'father_dob': 'Father Date of Birth',
        'father_mobile': 'Father Mobile',
        'father_pan': 'Father PAN',
        'father_aadhar': 'Father Aadhar',
        'father_height_weight': 'Father Height/Weight',
        'mother_name': 'Mother Name',
        'mother_dob': 'Mother Date of Birth',
        'mother_mobile': 'Mother Mobile',
        'mother_pan': 'Mother PAN',
        'mother_aadhar': 'Mother Aadhar',
        'mother_height_weight': 'Mother Height/Weight',
        'spouse_name': 'Spouse Name',
        'spouse_dob': 'Spouse Date of Birth',
        'spouse_mobile': 'Spouse Mobile',
        'spouse_pan': 'Spouse PAN',
        'spouse_aadhar': 'Spouse Aadhar',
        'spouse_height_weight': 'Spouse Height/Weight',
        'daughter_name': 'Daughter Name',
        'daughter_dob': 'Daughter Date of Birth',
        'daughter_mobile': 'Daughter Mobile',
        'daughter_pan': 'Daughter PAN',
        'daughter_aadhar': 'Daughter Aadhar',
        'daughter_height_weight': 'Daughter Height/Weight',
        'son_name': 'Son Name',
        'son_dob': 'Son Date of Birth',
        'son_mobile': 'Son Mobile',
        'son_pan': 'Son PAN',
        'son_aadhar': 'Son Aadhar',
        'son_height_weight': 'Son Height/Weight',
        'created_at': 'Date Added',
    },
    default_filename='contacts_export',
    sheet_name='Contacts',
)

def _populate_legacy_mandates_if_empty(contact):
    if contact.mandates.count() == 0:
        for provider, prefix in [('BSE', 'bse_mandate'), ('CAMS', 'cams_mandate'), ('KFIN', 'kfin_mandate'), ('NSE', 'nse_mandate')]:
            bank = getattr(contact, f'{prefix}_bank', '')
            m_id = getattr(contact, f'{prefix}_id', '')
            if bank or m_id:
                Mandate.objects.create(
                    contact=contact,
                    provider=provider,
                    bank_name=bank,
                    mandate_id=m_id,
                    mandate_limit=getattr(contact, f'{prefix}_limit', ''),
                    payer_name=getattr(contact, f'{prefix}_payer', ''),
                    umrn=getattr(contact, f'{prefix}_umrn', ''),
                )

@login_required
def contact_list_view(request):
    all_contacts = Contact.objects.all()
    contacts_qs = all_contacts.order_by('-created_at')
    contacts_qs, search_query = contact_searcher.search(request, contacts_qs)
    contacts_qs, active_filters = contact_filterer.filter(request, contacts_qs)

    return render(request, 'contacts/contact_list.html', {
        'contacts': contacts_qs,
        'search_query': search_query,
        'active_filters': active_filters,
        'selected_state': request.GET.get('state', ''),
        'selected_district': request.GET.get('district', ''),
        'selected_bank_type': request.GET.get('bank_account_type', ''),
        'selected_date_range': request.GET.get('created_at_range', request.GET.get('date_range', '')),
        'available_states': contact_filterer.get_distinct_values(all_contacts, 'state'),
        'available_districts': contact_filterer.get_distinct_values(all_contacts, 'district'),
        'available_bank_types': contact_filterer.get_distinct_values(all_contacts, 'bank_account_type'),
        'total_count': all_contacts.count(),
        'filtered_count': contacts_qs.count(),
    })

@login_required
def import_contacts_view(request):
    if request.method == 'POST':
        file_obj = request.FILES.get('import_file')
        if not file_obj:
            messages.error(request, 'Please select a CSV or Excel file to import.')
            return redirect('contacts:contact_list')

        result = contact_importer.import_file(file_obj, file_obj.name)

        if result.created > 0 or result.updated > 0:
            msg = f"Import completed: {result.created} contact(s) created, {result.updated} updated."
            if result.skipped > 0:
                msg += f" ({result.skipped} skipped)."
            messages.success(request, msg)
        elif result.errors:
            messages.error(request, f"Import failed: {'; '.join(result.errors[:3])}")
        else:
            messages.warning(request, "No contacts were imported from the file.")

    return redirect('contacts:contact_list')

@login_required
def export_contacts_view(request):
    export_format = request.GET.get('format', 'csv').lower()
    contacts_qs = Contact.objects.all().order_by('-created_at')
    contacts_qs, _ = contact_searcher.search(request, contacts_qs)
    contacts_qs, _ = contact_filterer.filter(request, contacts_qs)
    return contact_exporter.export_response(contacts_qs, format=export_format)

@login_required
def add_contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST, request.FILES)
        bank_formset = BankAccountFormSet(request.POST, request.FILES)
        family_formset = FamilyMemberFormSet(request.POST, request.FILES)
        nominee_formset = NomineeFormSet(request.POST, request.FILES)
        mandate_formset = MandateFormSet(request.POST, request.FILES)

        if form.is_valid() and bank_formset.is_valid() and family_formset.is_valid() and nominee_formset.is_valid() and mandate_formset.is_valid():
            contact = form.save()
            bank_formset.instance = contact
            bank_formset.save()
            family_formset.instance = contact
            family_formset.save()
            nominee_formset.instance = contact
            nominee_formset.save()
            mandate_formset.instance = contact
            mandate_formset.save()

            if contact.bank_accounts.count() == 0:
                if contact.savings_bank_name or contact.savings_account_no or contact.bank_name or contact.account_no:
                    BankAccount.objects.create(
                        contact=contact,
                        account_type=BankAccount.SAVINGS,
                        bank_name=contact.savings_bank_name or contact.bank_name,
                        account_no=contact.savings_account_no or contact.account_no,
                        ifsc_code=contact.savings_ifsc_code or contact.ifsc_code,
                        micr_code=contact.savings_micr_code or contact.micr_code,
                    )
                if contact.current_bank_name or contact.current_account_no:
                    BankAccount.objects.create(
                        contact=contact,
                        account_type=BankAccount.CURRENT,
                        bank_name=contact.current_bank_name,
                        account_no=contact.current_account_no,
                        ifsc_code=contact.current_ifsc_code,
                        micr_code=contact.current_micr_code,
                    )

            if contact.family_members.count() == 0:
                for rel, prefix in [('Father', 'father'), ('Mother', 'mother'), ('Spouse', 'spouse'), ('Daughter', 'daughter'), ('Son', 'son')]:
                    name = getattr(contact, f'{prefix}_name', '')
                    if name:
                        FamilyMember.objects.create(
                            contact=contact,
                            relationship=rel,
                            name=name,
                            dob=getattr(contact, f'{prefix}_dob', None),
                            mobile=getattr(contact, f'{prefix}_mobile', ''),
                            pan=getattr(contact, f'{prefix}_pan', ''),
                            aadhar=getattr(contact, f'{prefix}_aadhar', ''),
                            height_weight=getattr(contact, f'{prefix}_height_weight', ''),
                        )

            if contact.nominees.count() == 0 and contact.nominee_name:
                Nominee.objects.create(
                    contact=contact,
                    name=contact.nominee_name,
                    relationship=contact.nominee_relationship,
                    dob=contact.nominee_dob,
                    pan=contact.nominee_pan,
                    aadhar=contact.nominee_aadhar,
                    mobile=contact.nominee_mobile,
                    email=contact.nominee_email,
                )

            _populate_legacy_mandates_if_empty(contact)

            contact.sync_bank_accounts_to_legacy()
            contact.sync_family_members_to_legacy()
            contact.sync_nominees_to_legacy()
            contact.sync_mandates_to_legacy()
            messages.success(request, 'Contact added successfully.')
            return redirect('contacts:contact_list')
    else:
        form = ContactForm()
        bank_formset = BankAccountFormSet()
        family_formset = FamilyMemberFormSet()
        nominee_formset = NomineeFormSet()
        mandate_formset = MandateFormSet()
    return render(request, 'contacts/contact_form.html', {
        'form': form,
        'bank_formset': bank_formset,
        'family_formset': family_formset,
        'nominee_formset': nominee_formset,
        'mandate_formset': mandate_formset,
    })

@login_required
def edit_contact_view(request, pk):
    contact = get_object_or_404(Contact, pk=pk)
    if request.method == 'POST':
        form = ContactForm(request.POST, request.FILES, instance=contact)
        bank_formset = BankAccountFormSet(request.POST, request.FILES, instance=contact)
        family_formset = FamilyMemberFormSet(request.POST, request.FILES, instance=contact)
        nominee_formset = NomineeFormSet(request.POST, request.FILES, instance=contact)
        mandate_formset = MandateFormSet(request.POST, request.FILES, instance=contact)

        if form.is_valid() and bank_formset.is_valid() and family_formset.is_valid() and nominee_formset.is_valid() and mandate_formset.is_valid():
            contact = form.save()
            bank_formset.save()
            family_formset.save()
            nominee_formset.save()
            mandate_formset.save()

            if contact.bank_accounts.count() == 0:
                if contact.savings_bank_name or contact.savings_account_no or contact.bank_name or contact.account_no:
                    BankAccount.objects.create(
                        contact=contact,
                        account_type=BankAccount.SAVINGS,
                        bank_name=contact.savings_bank_name or contact.bank_name,
                        account_no=contact.savings_account_no or contact.account_no,
                        ifsc_code=contact.savings_ifsc_code or contact.ifsc_code,
                        micr_code=contact.savings_micr_code or contact.micr_code,
                    )
                if contact.current_bank_name or contact.current_account_no:
                    BankAccount.objects.create(
                        contact=contact,
                        account_type=BankAccount.CURRENT,
                        bank_name=contact.current_bank_name,
                        account_no=contact.current_account_no,
                        ifsc_code=contact.current_ifsc_code,
                        micr_code=contact.current_micr_code,
                    )

            if contact.family_members.count() == 0:
                for rel, prefix in [('Father', 'father'), ('Mother', 'mother'), ('Spouse', 'spouse'), ('Daughter', 'daughter'), ('Son', 'son')]:
                    name = getattr(contact, f'{prefix}_name', '')
                    if name:
                        FamilyMember.objects.create(
                            contact=contact,
                            relationship=rel,
                            name=name,
                            dob=getattr(contact, f'{prefix}_dob', None),
                            mobile=getattr(contact, f'{prefix}_mobile', ''),
                            pan=getattr(contact, f'{prefix}_pan', ''),
                            aadhar=getattr(contact, f'{prefix}_aadhar', ''),
                            height_weight=getattr(contact, f'{prefix}_height_weight', ''),
                        )

            if contact.nominees.count() == 0 and contact.nominee_name:
                Nominee.objects.create(
                    contact=contact,
                    name=contact.nominee_name,
                    relationship=contact.nominee_relationship,
                    dob=contact.nominee_dob,
                    pan=contact.nominee_pan,
                    aadhar=contact.nominee_aadhar,
                    mobile=contact.nominee_mobile,
                    email=contact.nominee_email,
                )

            _populate_legacy_mandates_if_empty(contact)

            contact.sync_bank_accounts_to_legacy()
            contact.sync_family_members_to_legacy()
            contact.sync_nominees_to_legacy()
            contact.sync_mandates_to_legacy()
            messages.success(request, 'Contact updated successfully.')
            return redirect('contacts:contact_list')
    else:
        form = ContactForm(instance=contact)
        if contact.bank_accounts.count() == 0:
            if contact.savings_bank_name or contact.savings_account_no or contact.bank_name or contact.account_no:
                BankAccount.objects.create(
                    contact=contact,
                    account_type=BankAccount.SAVINGS,
                    bank_name=contact.savings_bank_name or contact.bank_name,
                    account_no=contact.savings_account_no or contact.account_no,
                    ifsc_code=contact.savings_ifsc_code or contact.ifsc_code,
                    micr_code=contact.savings_micr_code or contact.micr_code,
                )
            if contact.current_bank_name or contact.current_account_no:
                BankAccount.objects.create(
                    contact=contact,
                    account_type=BankAccount.CURRENT,
                    bank_name=contact.current_bank_name,
                    account_no=contact.current_account_no,
                    ifsc_code=contact.current_ifsc_code,
                    micr_code=contact.current_micr_code,
                )

        if contact.family_members.count() == 0:
            for rel, prefix in [('Father', 'father'), ('Mother', 'mother'), ('Spouse', 'spouse'), ('Daughter', 'daughter'), ('Son', 'son')]:
                name = getattr(contact, f'{prefix}_name', '')
                if name:
                    FamilyMember.objects.create(
                        contact=contact,
                        relationship=rel,
                        name=name,
                        dob=getattr(contact, f'{prefix}_dob', None),
                        mobile=getattr(contact, f'{prefix}_mobile', ''),
                        pan=getattr(contact, f'{prefix}_pan', ''),
                        aadhar=getattr(contact, f'{prefix}_aadhar', ''),
                        height_weight=getattr(contact, f'{prefix}_height_weight', ''),
                    )

        if contact.nominees.count() == 0 and contact.nominee_name:
            Nominee.objects.create(
                contact=contact,
                name=contact.nominee_name,
                relationship=contact.nominee_relationship,
                dob=contact.nominee_dob,
                pan=contact.nominee_pan,
                aadhar=contact.nominee_aadhar,
                mobile=contact.nominee_mobile,
                email=contact.nominee_email,
            )

        _populate_legacy_mandates_if_empty(contact)

        bank_formset = BankAccountFormSet(instance=contact)
        family_formset = FamilyMemberFormSet(instance=contact)
        nominee_formset = NomineeFormSet(instance=contact)
        mandate_formset = MandateFormSet(instance=contact)
    return render(request, 'contacts/contact_form.html', {
        'form': form,
        'contact': contact,
        'bank_formset': bank_formset,
        'family_formset': family_formset,
        'nominee_formset': nominee_formset,
    })


@login_required
def delete_contact_view(request, pk):
    contact = get_object_or_404(Contact, pk=pk)
    if request.method == 'POST':
        name = contact.name
        contact.delete()
        messages.success(request, f'Contact "{name}" deleted successfully.')
    return redirect('contacts:contact_list')









