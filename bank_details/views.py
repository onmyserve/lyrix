from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q
import urllib.request
import json

from .models import BankDetail
from .forms import BankDetailForm
from utils.search import ModelSearcher
from utils.importer import ModelFileImporter
from utils.exporter import ModelFileExporter
from utils.filters import ModelFilterer


bank_detail_searcher = ModelSearcher(
    search_fields=['bank_name', 'ifsc_code', 'micr_code', 'branch_name'],
    param_name='q'
)

bank_detail_filterer = ModelFilterer(
    exact_fields=['bank_name'],
    date_fields=['created_at']
)

bank_detail_importer = ModelFileImporter(
    model_class=BankDetail,
    field_mapping={
        'bank_name': ['bank_name', 'bank', 'bank name'],
        'ifsc_code': ['ifsc_code', 'ifsc', 'ifsc code'],
        'micr_code': ['micr_code', 'micr', 'micr code'],
        'branch_name': ['branch_name', 'branch', 'branch name'],
    },
    required_fields=['bank_name', 'ifsc_code'],
    unique_key='ifsc_code',
    update_existing=True,
)

bank_detail_exporter = ModelFileExporter(
    model_class=BankDetail,
    header_labels={
        'id': 'ID',
        'bank_name': 'Bank Name',
        'ifsc_code': 'IFSC Code',
        'micr_code': 'MICR Code',
        'branch_name': 'Branch Name',
        'created_at': 'Date Added',
    },
    default_filename='bank_details_export',
    sheet_name='Bank Details',
)


@login_required
def bank_detail_list_view(request):
    all_banks = BankDetail.objects.all()
    banks_qs = all_banks.order_by('-created_at')
    banks_qs, search_query = bank_detail_searcher.search(request, banks_qs)
    banks_qs, active_filters = bank_detail_filterer.filter(request, banks_qs)

    available_bank_names = bank_detail_filterer.get_distinct_values(all_banks, 'bank_name')

    total_count = all_banks.count()
    unique_banks_count = len(available_bank_names)
    ifsc_count = all_banks.exclude(ifsc_code='').count()
    micr_count = all_banks.exclude(micr_code='').count()

    return render(request, 'bank_details/bank_detail_list.html', {
        'bank_details': banks_qs,
        'search_query': search_query,
        'active_filters': active_filters,
        'selected_bank': request.GET.get('bank_name', ''),
        'selected_date_range': request.GET.get('created_at_range', request.GET.get('date_range', '')),
        'available_bank_names': available_bank_names,
        'total_count': total_count,
        'filtered_count': banks_qs.count(),
        'unique_banks_count': unique_banks_count,
        'ifsc_count': ifsc_count,
        'micr_count': micr_count,
    })


@login_required
def add_bank_detail_view(request):
    if request.method == 'POST':
        form = BankDetailForm(request.POST)
        if form.is_valid():
            bank = form.save()
            messages.success(request, f'Bank detail for "{bank.bank_name} ({bank.ifsc_code})" added successfully.')
            return redirect('bank_details:list')
    else:
        form = BankDetailForm()

    return render(request, 'bank_details/bank_detail_form.html', {
        'form': form,
        'is_edit': False,
    })


@login_required
def edit_bank_detail_view(request, pk):
    bank = get_object_or_404(BankDetail, pk=pk)
    if request.method == 'POST':
        form = BankDetailForm(request.POST, instance=bank)
        if form.is_valid():
            form.save()
            messages.success(request, f'Bank detail for "{bank.bank_name} ({bank.ifsc_code})" updated successfully.')
            return redirect('bank_details:list')
    else:
        form = BankDetailForm(instance=bank)

    return render(request, 'bank_details/bank_detail_form.html', {
        'form': form,
        'bank': bank,
        'is_edit': True,
    })


@login_required
def delete_bank_detail_view(request, pk):
    bank = get_object_or_404(BankDetail, pk=pk)
    if request.method == 'POST':
        bank_name = bank.bank_name
        ifsc = bank.ifsc_code
        bank.delete()
        messages.success(request, f'Bank detail for "{bank_name} ({ifsc})" deleted successfully.')
    return redirect('bank_details:list')


@login_required
def import_bank_details_view(request):
    if request.method == 'POST':
        file_obj = request.FILES.get('import_file')
        if not file_obj:
            messages.error(request, 'Please select a CSV or Excel file to import.')
            return redirect('bank_details:list')

        result = bank_detail_importer.import_file(file_obj, file_obj.name)

        if result.created > 0 or result.updated > 0:
            msg = f"Import completed: {result.created} bank record(s) created, {result.updated} updated."
            if result.skipped > 0:
                msg += f" ({result.skipped} skipped)."
            messages.success(request, msg)
        elif result.errors:
            messages.error(request, f"Import failed: {'; '.join(result.errors[:3])}")
        else:
            messages.warning(request, "No bank records were imported from the file.")

    return redirect('bank_details:list')


@login_required
def export_bank_details_view(request):
    export_format = request.GET.get('format', 'csv').lower()
    banks_qs = BankDetail.objects.all().order_by('-created_at')
    banks_qs, _ = bank_detail_searcher.search(request, banks_qs)
    banks_qs, _ = bank_detail_filterer.filter(request, banks_qs)
    return bank_detail_exporter.export_response(banks_qs, format=export_format)


@login_required
def bank_detail_lookup_api(request):
    ifsc = request.GET.get('ifsc', '').strip().upper()
    q = request.GET.get('q', '').strip()

    if ifsc:
        bank = BankDetail.objects.filter(ifsc_code__iexact=ifsc).first()
        if bank:
            return JsonResponse({
                'found': True,
                'bank_name': bank.bank_name,
                'ifsc_code': bank.ifsc_code,
                'micr_code': bank.micr_code,
                'branch_name': bank.branch_name,
                'source': 'database',
            })
        
        try:
            url = f"https://ifsc.razorpay.com/{ifsc}"
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=3) as resp:
                if resp.status == 200:
                    data = json.loads(resp.read().decode('utf-8'))
                    return JsonResponse({
                        'found': True,
                        'bank_name': data.get('BANK', ''),
                        'ifsc_code': data.get('IFSC', ifsc),
                        'micr_code': str(data.get('MICR', '') or ''),
                        'branch_name': data.get('BRANCH', ''),
                        'source': 'api',
                    })
        except Exception:
            pass

        return JsonResponse({'found': False})

    if q:
        banks = BankDetail.objects.filter(
            Q(bank_name__icontains=q) | Q(ifsc_code__icontains=q) | Q(micr_code__icontains=q)
        )[:15]
        results = [
            {
                'bank_name': b.bank_name,
                'ifsc_code': b.ifsc_code,
                'micr_code': b.micr_code,
                'branch_name': b.branch_name,
            }
            for b in banks
        ]
        return JsonResponse({'results': results})

    all_banks = BankDetail.objects.all().values('bank_name', 'ifsc_code', 'micr_code', 'branch_name')
    return JsonResponse({'results': list(all_banks)})
