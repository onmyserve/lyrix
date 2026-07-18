from django.shortcuts import render, redirect
from .models import UserProfile
from .forms import UserProfileForm

def home_view(request):
    # Query all users from the database
    users = UserProfile.objects.all()
    return render(request, 'home.html', {'users': users})

def add_user_view(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST)
        if form.is_valid():
            form.save()  # This inserts the row directly into PostgreSQL
            return redirect('add_user')  # Redirects back to the same page to clear the form
    else:
        form = UserProfileForm()
        
    return render(request, 'add_user.html', {'form': form})
