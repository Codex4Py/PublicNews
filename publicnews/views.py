# views.py

from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as auth_login

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)  # Log the user in after signup
            return redirect('home')  # Redirect to a desired page
    else:
        form = UserCreationForm()
    
    return render(request, 'registration/signup.html', {'form': form})
