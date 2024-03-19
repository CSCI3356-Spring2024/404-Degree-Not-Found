from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic 
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.urls import reverse_lazy
from .models import Name
from django.contrib.auth import login

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('landing')  # Redirect to your landing page
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('landing')  # Redirect to your landing page
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def landing_view(request, *args, **kwargs):
	print(args, kwargs)
	print(request.user)
 	#return HttpResponse('<h1>Hello World</h1>') #string of HTML code
	return render(request, 'Landing.html', {}) 

def profile_view(request):
    return render(request, 'profile.html', {})

def future_plan_view(request):
    return render(request, 'future_plan.html', {})
