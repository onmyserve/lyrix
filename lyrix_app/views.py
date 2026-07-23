from django.shortcuts import render, redirect
from .models import UserProfile, Customer
from .forms import UserProfileForm, CustomerForm
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied


@login_required
def home_view(request):
    # Query all users from the database
    users = UserProfile.objects.all()
    return render(request, 'lyrix_app/home.html', {'users': users})

def add_user_view(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST)
        if form.is_valid():
            form.save()  # This inserts the row directly into PostgreSQL
            return redirect('add_user')  # Redirects back to the same page to clear the form
    else:
        form = UserProfileForm()
        
    return render(request, 'lyrix_app/add_user.html', {'form': form})

@login_required
def customer_list_view(request): # Renamed
    customers = Customer.objects.all()
    return render(request, 'lyrix_app/contact/contact_list.html', {'customers': customers})


def add_customer_view(request): # Renamed
    #if not request.user.is_staff:
    #    raise PermissionDenied
        
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('customer_list') # Redirect to new URL name
    else:
        form = CustomerForm()
    return render(request, 'lyrix_app/contact/contact_form.html', {'form': form})