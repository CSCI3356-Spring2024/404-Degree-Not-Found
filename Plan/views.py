from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic 
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.urls import reverse_lazy
from django.contrib.auth import login
from .forms import EditStudentInfo
from .models import Student, Admin

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            role = request.POST.get('role')
            user = form.save()
            if role == 'student':
                # Create a Student instance if the role is 'student'
                Student.objects.create(user=user, major='Computer Science', grad_year='2025', entered='2021')
            elif role == 'admin':
                # Create an Admin instance if the role is 'admin'
                Admin.objects.create(user=user)
                # Additional logic for admin role if needed
            #elif role == 'advisor':
                # Create an Advisor instance if the role is 'advisor'
                #Advisor.objects.create(user=user)
                # Additional logic for advisor role if needed
            login(request, user)
            return redirect('Plan:landing')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('Plan:landing')  
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def landing_view(request):
    user = request.user
    try:
        student = Student.objects.get(email=user.email)
    except Student.DoesNotExist:
        new_student = Student(first_name=user.first_name, email=user.email)
        new_student.save()
 	#return HttpResponse('<h1>Hello World</h1>') #string of HTML code
    return render(request, 'Landing.html', {}) 

def profile_view(request):
    user = request.user
    student = Student.objects.get(email=user.email)
    if request.method == 'POST':
        form = EditStudentInfo(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect('Plan:landing') 
    else:
        form = EditStudentInfo(instance=student)
    
    return render(request, 'profile.html', {'form': form})

def future_plan_view(request):
    return render(request, 'futureplan.html', {})
