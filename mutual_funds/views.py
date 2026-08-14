from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from contacts.models import Contact
from .models import MutualFund
from .forms import MutualFundForm
from utils.search import ModelSearcher
from utils.importer import parse_imported_file, ImportResult
from utils.exporter import ModelFileExporter
from utils.filters import ModelFilterer

mf_searcher = ModelSearcher(
    search_fields=[
        'name', 'mobile_no', 'pan', 'amc', 'fund_description',
        'folio_number', 'mandate_id', 'bank', 'transaction_id',
        'amount', 'remarks', 'transaction_description',
        'contact__name', 'contact__mobile_no', 'contact__email'
    ],
    param_name='q'
)

mf_filterer = ModelFilterer(
    exact_fields=['amc', 'mode', 'bank'],
    date_fields=['created_at', 'transaction_date', 'process_date']
)

mf_exporter = ModelFileExporter(
    model_class=MutualFund,
    header_labels={
        'id': 'ID',
        'name': 'Name',
        'mobile_no': 'Mobile Number',
        'pan': 'PAN',
        'amc': 'AMC',
        'fund_description': 'Fund Description',
        'folio_number': 'Folio Number',
        'sip_amt': 'SIP Amount',
        'sip_date': 'SIP Date',
        'mode': 'Mode',
        'sip_start_date': 'SIP Start Date',
        'sip_end_date': 'SIP End Date',
        'bank': 'Bank',
        'mandate_id': 'Mandate ID',
        'transaction_date': 'Transaction Date',
        'amount': 'Amount',
        'stamp_duty': 'Stamp Duty',
        'process_date': 'Process Date',
        'price': 'Price',
        'units': 'Units',
        'remarks': 'Remarks',
        'transaction_description': 'Transaction Description',
        'transaction_id': 'Transaction ID',
        'created_at': 'Date Added',
    },
    default_filename='mutual_funds_export',
    sheet_name='Mutual Funds',
)


@login_required
def mutual_fund_list_view(request):
    all_funds = MutualFund.objects.select_related('contact').all()
    funds_qs = all_funds.order_by('-created_at')
    funds_qs, search_query = mf_searcher.search(request, funds_qs)
    funds_qs, active_filters = mf_filterer.filter(request, funds_qs)

    available_amcs = mf_filterer.get_distinct_values(all_funds, 'amc')
    available_modes = mf_filterer.get_distinct_values(all_funds, 'mode')
    available_banks = mf_filterer.get_distinct_values(all_funds, 'bank')

    return render(request, 'mutual_funds/mutual_fund_list.html', {
        'mutual_funds': funds_qs,
        'search_query': search_query,
        'active_filters': active_filters,
        'selected_amc': request.GET.get('amc', ''),
        'selected_mode': request.GET.get('mode', ''),
        'selected_bank': request.GET.get('bank', ''),
        'selected_date_range': request.GET.get('created_at_range', request.GET.get('date_range', '')),
        'available_amcs': available_amcs,
        'available_modes': available_modes,
        'available_banks': available_banks,
        'total_count': all_funds.count(),
        'filtered_count': funds_qs.count(),
    })


@login_required
def add_mutual_fund_view(request):
    contacts_exist = Contact.objects.exists()

    if request.method == 'POST':
        form = MutualFundForm(request.POST)
        if form.is_valid():
            fund = form.save()
            messages.success(request, f'Mutual fund record for "{fund.name or fund.contact.name}" added successfully.')
            return redirect('mutual_funds:fund_list')
    else:
        initial_data = {}
        contact_id = request.GET.get('contact_id')
        if contact_id:
            contact = Contact.objects.filter(pk=contact_id).first()
            if contact:
                initial_data = {
                    'contact': contact.pk,
                    'name': contact.name,
                    'mobile_no': contact.mobile_no,
                    'pan': getattr(contact, 'pan_no', ''),
                }
        form = MutualFundForm(initial=initial_data)

    return render(request, 'mutual_funds/mutual_fund_form.html', {
        'form': form,
        'is_edit': False,
        'contacts_exist': contacts_exist,
    })


@login_required
def edit_mutual_fund_view(request, pk):
    fund = get_object_or_404(MutualFund, pk=pk)
    contacts_exist = Contact.objects.exists()

    if request.method == 'POST':
        form = MutualFundForm(request.POST, instance=fund)
        if form.is_valid():
            form.save()
            messages.success(request, f'Mutual fund record for "{fund.name or fund.contact.name}" updated successfully.')
            return redirect('mutual_funds:fund_list')
    else:
        form = MutualFundForm(instance=fund)

    return render(request, 'mutual_funds/mutual_fund_form.html', {
        'form': form,
        'fund': fund,
        'is_edit': True,
        'contacts_exist': contacts_exist,
    })


@login_required
def import_mutual_funds_view(request):
    if request.method == 'POST':
        file_obj = request.FILES.get('import_file')
        if not file_obj:
            messages.error(request, 'Please select a CSV or Excel file to import.')
            return redirect('mutual_funds:fund_list')

        result = process_mutual_fund_import(file_obj, file_obj.name)

        if result.created > 0 or result.updated > 0:
            msg = f"Import completed: {result.created} mutual fund record(s) created."
            if result.skipped > 0:
                msg += f" ({result.skipped} skipped)."
            messages.success(request, msg)
        elif result.errors:
            messages.error(request, f"Import failed: {'; '.join(result.errors[:3])}")
        else:
            messages.warning(request, "No mutual fund records were imported from the file.")

    return redirect('mutual_funds:fund_list')


def process_mutual_fund_import(file_obj, filename):
    result = ImportResult()
    try:
        raw_rows = parse_imported_file(file_obj, filename)
    except Exception as e:
        result.errors.append(f"File parsing error: {str(e)}")
        return result

    if not raw_rows:
        result.errors.append("The uploaded file is empty or has no data rows.")
        return result

    result.total = len(raw_rows)

    with transaction.atomic():
        for idx, row in enumerate(raw_rows, start=1):
            row_data = {}
            mobile = ''
            email = ''
            name = ''

            for k, v in row.items():
                val_str = str(v).strip() if v is not None else ''
                k_clean = k.strip().lower().replace(' ', '').replace('_', '').replace('-', '')

                if k_clean in ('mobile', 'mobileno', 'phone', 'phonenumber', 'contact'):
                    mobile = val_str
                    row_data['mobile_no'] = val_str
                elif k_clean in ('email', 'emailaddress', 'mail'):
                    email = val_str
                elif k_clean in ('name', 'fullname', 'investorname', 'clientname'):
                    name = val_str
                    row_data['name'] = val_str
                elif k_clean in ('pan', 'panno', 'pannumber'):
                    row_data['pan'] = val_str
                elif k_clean in ('sipamt', 'sipamount'):
                    row_data['sip_amt'] = val_str
                elif k_clean in ('sipdate',):
                    row_data['sip_date'] = val_str
                elif k_clean in ('mode', 'sipmode'):
                    row_data['mode'] = val_str
                elif k_clean in ('bank', 'bankname'):
                    row_data['bank'] = val_str
                elif k_clean in ('mandateid', 'mandate'):
                    row_data['mandate_id'] = val_str
                elif k_clean in ('amc', 'amcname'):
                    row_data['amc'] = val_str
                elif k_clean in ('funddescription', 'description', 'fund', 'schemename'):
                    row_data['fund_description'] = val_str
                elif k_clean in ('folionumber', 'folio', 'foliono'):
                    row_data['folio_number'] = val_str
                elif k_clean in ('transactiondate', 'txndate'):
                    row_data['transaction_date'] = val_str
                elif k_clean in ('amount', 'amt', 'txnamount'):
                    row_data['amount'] = val_str
                elif k_clean in ('stampduty', 'stamp'):
                    row_data['stamp_duty'] = val_str
                elif k_clean in ('processdate', 'procdate'):
                    row_data['process_date'] = val_str
                elif k_clean in ('price', 'nav'):
                    row_data['price'] = val_str
                elif k_clean in ('units', 'unit'):
                    row_data['units'] = val_str
                elif k_clean in ('remarks', 'remark'):
                    row_data['remarks'] = val_str
                elif k_clean in ('transactiondescription', 'txndescription', 'txndesc'):
                    row_data['transaction_description'] = val_str
                elif k_clean in ('transactionid', 'txnid'):
                    row_data['transaction_id'] = val_str

            contact = None
            if mobile:
                contact = Contact.objects.filter(mobile_no=mobile).first()
            if not contact and email:
                contact = Contact.objects.filter(email__iexact=email).first()
            if not contact and name:
                contact = Contact.objects.filter(name__iexact=name).first()

            if not contact:
                identifier = name or mobile or email or f"Row {idx}"
                result.errors.append(
                    f"Row {idx}: Contact '{identifier}' not found in Contacts. Mutual funds can only be added for existing contacts."
                )
                result.skipped += 1
                continue

            row_data['contact'] = contact
            if 'name' not in row_data or not row_data['name']:
                row_data['name'] = contact.name
            if 'mobile_no' not in row_data or not row_data['mobile_no']:
                row_data['mobile_no'] = contact.mobile_no
            if 'pan' not in row_data or not row_data['pan']:
                row_data['pan'] = getattr(contact, 'pan_no', '')

            MutualFund.objects.create(**row_data)
            result.created += 1

    return result


@login_required
def export_mutual_funds_view(request):
    export_format = request.GET.get('format', 'csv').lower()
    funds_qs = MutualFund.objects.select_related('contact').all().order_by('-created_at')
    funds_qs, _ = mf_searcher.search(request, funds_qs)
    funds_qs, _ = mf_filterer.filter(request, funds_qs)
    return mf_exporter.export_response(funds_qs, format=export_format)


@login_required
def delete_mutual_fund_view(request, pk):
    fund = get_object_or_404(MutualFund, pk=pk)
    if request.method == 'POST':
        name = fund.name or (fund.contact.name if fund.contact else 'Record')
        fund.delete()
        messages.success(request, f'Mutual fund record for "{name}" deleted successfully.')
    return redirect('mutual_funds:fund_list')

