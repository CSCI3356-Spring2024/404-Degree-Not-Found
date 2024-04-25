from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic 
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.urls import reverse_lazy
from django.contrib.auth import login, logout
from .forms import EditStudentInfo, AddCourseToPlan
from .models import Student, Admin, Plan
from .api import fetch_course_data, fetch_courses
from django.core.paginator import Paginator
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from .data import MAJOR_COURSE_MAP
from django.core.exceptions import ValidationError


def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            role = request.POST.get('role')
            fname = request.POST.get('first_name')
            lname = request.POST.get('last_name')
            user = form.save()
            if role == 'student':
                # Create a Student instance if the role is 'student'
                Student.objects.create(first_name=fname, last_name=lname)
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
        student = Student(first_name=user.first_name, last_name=user.last_name, email=user.email)
        student.save()
        return redirect('Plan:profile')

    return render(request, 'Landing.html', {'student': student}) 

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
    
    return render(request, 'profile.html', {'form': form, 'student': student})

def unique_semesters_needed(request):
    return request.GET.get('unique_semesters', 'false') == 'true'

def logout_view(request):
    logout(request)
    return redirect("/")

def courseview(request, course_code):
    course_details = fetch_course_data(course_code)
    return render(request, 'course_detail.html', {'course': course_details})

def future_plan_view(request, plan_number):
    user = request.user
    student = Student.objects.get(email=user.email)

    return render(request, 'futureplan.html', {'student': student})


def course_list_view(request):
    user = request.user
    student = Student.objects.get(email=user.email)
    course_code = request.GET.get('course_code', '')
    courses_list = fetch_courses(course_code) if course_code else []

    paginator = Paginator(courses_list, 10)  # Show 10 courses per page.
    page_number = request.GET.get('page')
    courses = paginator.get_page(page_number)

    if student.plan_set.count() < 3:
        for _ in range(3 - student.plan_set.count()):
            Plan.objects.create(student=student)
        
    if request.method == 'POST':
        form = AddCourseToPlan(request.POST, student=student)
        if form.is_valid():
            try:
                form.save(student)
                print("Form data:", form.cleaned_data)
                print("Course added to the plan successfully.")
            except ValidationError as e:
                return render(request, 'course_list.html', {
                    'courses': courses,
                    'course_code': course_code,
                    'student': student,
                    'form': form,
                    'error_message': e.message,
                })
        else:
            form = AddCourseToPlan(student=student)
            print("Form errors:", form.errors)
            print("Course not added to plan")
    else:
        form = AddCourseToPlan(student=student) 
        print("Request method is not POST")

    return render(request, 'course_list.html', {
        'courses': courses,
        'course_code': course_code,
        'student': student,
        'form': form, 
    })

def reqs_list_view(request):
    major = request.GET.get('major', '')
    all_courses = []

    if major in MAJOR_COURSE_MAP:
        course_codes = MAJOR_COURSE_MAP[major]
        for code in course_codes:
            courses_for_code = fetch_courses(code)
            all_courses.extend(courses_for_code) 

    page_number = request.GET.get('page', 1)
    paginator = Paginator(all_courses, 10)  # Show 10 courses per page
    page_obj = paginator.get_page(page_number)

    return render(request, 'reqs_list.html', {
        'major': major,
        'page_obj': page_obj, 
        'MAJOR_COURSE_MAP': MAJOR_COURSE_MAP
    })


