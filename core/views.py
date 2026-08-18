from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import UserProfile, Customer
from .forms import UserProfileForm, CustomerForm


@login_required
def home_view(request):
    users = UserProfile.objects.all()
    return render(request, 'core/home.html', {'users': users})


def add_user_view(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('add_user')
    else:
        form = UserProfileForm()
    return render(request, 'core/add_user.html', {'form': form})


@login_required
def customer_list_view(request):
    return redirect('contacts:contact_list')


def add_customer_view(request):
    return redirect('contacts:add_contact')