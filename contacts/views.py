from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Contact
from .forms import ContactForm
from utils.search import ModelSearcher
from utils.importer import ModelFileImporter
from utils.exporter import ModelFileExporter
from utils.filters import ModelFilterer

contact_searcher = ModelSearcher(
    search_fields=['first_name', 'last_name', 'email'],
    param_name='q'
)

contact_filterer = ModelFilterer(
    exact_fields=[],
    date_fields=['created_at']
)

contact_importer = ModelFileImporter(
    model_class=Contact,
    field_mapping={
        'first_name': ['first_name', 'first name', 'fname', 'given name', 'name'],
        'last_name': ['last_name', 'last name', 'lname', 'surname', 'family name'],
        'email': ['email', 'email address', 'e-mail', 'mail'],
    },
    required_fields=['first_name', 'email'],
    unique_key='email',
    update_existing=True,
    default_values={}
)

contact_exporter = ModelFileExporter(
    fields=['first_name', 'last_name', 'email', 'created_at'],
    header_labels={
        'first_name': 'First Name',
        'last_name': 'Last Name',
        'email': 'Email Address',
        'created_at': 'Date Added',
    },
    default_filename='contacts_export',
    sheet_name='Contacts',
)

@login_required
def contact_list_view(request):
    contacts_qs = Contact.objects.all().order_by('-created_at')
    contacts_qs, search_query = contact_searcher.search(request, contacts_qs)
    contacts_qs, active_filters = contact_filterer.filter(request, contacts_qs)

    return render(request, 'contacts/contact_list.html', {
        'contacts': contacts_qs,
        'search_query': search_query,
        'active_filters': active_filters,
        'selected_date_range': request.GET.get('created_at_range', request.GET.get('date_range', '')),
        'total_count': Contact.objects.count(),
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
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Contact added successfully.')
            return redirect('contacts:contact_list')
    else:
        form = ContactForm()
    return render(request, 'contacts/contact_form.html', {'form': form})



