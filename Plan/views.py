from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic 
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.urls import reverse_lazy
from django.contrib.auth import login, logout
from .forms import EditStudentInfo, AddCourseToPlan
from .models import Student, Admin, Course, Plan, Semester
from .api import fetch_course_data, fetch_courses
from django.core.paginator import Paginator
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from .data import MAJOR_COURSE_MAP

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
    try:
        student = Student.objects.get(email=user.email)
    except Student.DoesNotExist:
        return render(request, 'error.html', {'message': 'Student not found'})

    # Check if the plan exists, if not, create it
    plan_instances = Plan.objects.filter(user=student)
    if not plan_instances.exists():
        for plan_number in range(1, 4):
            Plan.objects.create(user=student, plan_number=plan_number)

    # Retrieve the specific plan based on the plan number
    try:
        plan = Plan.objects.get(user=student, plan_number=plan_number)
    except Plan.DoesNotExist:
        return render(request, 'error.html', {'message': 'Plan not found'})

    # Retrieve all semesters associated with the plan
    semesters = plan.semesters.all()

    return render(request, 'futureplan.html', {'student': student, 'semesters': semesters})


def course_list_view(request):
    user = request.user
    student = Student.objects.get(email=user.email)
    course_code = request.GET.get('course_code', '')
    courses_list = fetch_courses(course_code) if course_code else []

    paginator = Paginator(courses_list, 10)  # Show 10 courses per page.
    page_number = request.GET.get('page')
    courses = paginator.get_page(page_number)

    # Fetch plan instances for the student
    plan_instances = Plan.objects.filter(user=student)
    semester_instances = Semester.objects.all()

    if request.method == 'POST':
        form = AddCourseToPlan(request.POST)
        print("POST data:", request.POST)

        if form.is_valid():
            print("Form is valid.")
            course, semester = form.save(student)
            print(course)
            print(semester)
        else:
            print("Form is not valid:", form.errors)

    else:
        form = AddCourseToPlan()

    return render(request, 'course_list.html', {
        'courses': courses,
        'course_code': course_code,
        'student': student,
        'form': form,
        'plans': plan_instances,
        'semester': semester_instances, 
    })

def reqs_list_view(request):
    major = request.GET.get('major', '')
    courses_details = []

    if major in MAJOR_COURSE_MAP:
        course_codes = MAJOR_COURSE_MAP[major]
        courses_details = [fetch_course_data(code) for code in course_codes if fetch_course_data(code)]

    return render(request, 'reqs_list.html', {
        'major': major,
        'courses': courses_details,
        'MAJOR_COURSE_MAP' : MAJOR_COURSE_MAP
    })


