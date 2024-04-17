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

def future_plan_view(request):
    user = request.user
    try:
        student = Student.objects.get(email=user.email)
    except Student.DoesNotExist:
        return render(request, 'error.html', {'message': 'Student not found'})

    needs_unique_semesters = request.GET.get('unique_semesters', 'false') == 'true'

    if not Plan.objects.filter(user=student).exists():
        new_plan = Plan(user=student)

        if needs_unique_semesters:
            # Create new semester instances to ensure they are unique
            for i in range(1, 9):
                semester = Semester.objects.create(semester_number=Semester.objects.count() + 1)
                setattr(new_plan, f'semester_{i}', semester)
        else:
            # Attempt to reuse semesters; this block needs careful handling
            # to ensure it doesn't violate the unique constraint
            for i in range(1, 9):
                semester, _ = Semester.objects.get_or_create(semester_number=i)
                setattr(new_plan, f'semester_{i}', semester)

        new_plan.save()

    return render(request, 'futureplan.html', {'student': student})

def semester_is_linked(semester):
    return any([
        hasattr(semester, 'freshman_fall'),
        hasattr(semester, 'freshman_spring'),
        hasattr(semester, 'sophomore_fall'),
        hasattr(semester, 'sophomore_spring'),
        hasattr(semester, 'junior_fall'),
        hasattr(semester, 'junior_spring'),
        hasattr(semester, 'senior_fall'),
        hasattr(semester, 'senior_spring'),
    ])

# def courses_view(request):
#     return render(request, 'Courses.html', {})

def logout_view(request):
    logout(request)
    return redirect("/")

def courseview(request, course_code):
    course_details = fetch_course_data(course_code)
    return render(request, 'course_detail.html', {'course': course_details})


def course_list_view(request):
    user = request.user
    student = Student.objects.get(email=user.email)

    course_code = request.GET.get('course_code', '')
    courses_list = fetch_courses(course_code) if course_code else []

    paginator = Paginator(courses_list, 10)  # Show 10 courses per page.

    page_number = request.GET.get('page')
    courses = paginator.get_page(page_number)

    if request.method == 'POST':
        form = AddCourseToPlan(request.POST, student=student)
        if form.is_valid():
            course_id = request.POST.get('course_id')
            semester_number = request.POST.get('semester_number')
            plan_id = request.POST.get('plan_id')

            try:
                plan = Plan.objects.get(id=plan_id, student=student)
                course = Course.objects.get(id=course_id)
                add_course_view(plan, course, semester_number)
                return redirect('Plan:course_list')  # Redirect to the course list page
            except (Plan.DoesNotExist, Course.DoesNotExist):
                return HttpResponseBadRequest("Invalid data provided.")
    plans = Plan.objects.filter(user=student)
    form = AddCourseToPlan(student=student, plans=plans)
    return render(request, 'course_list.html', {'courses': courses, 'course_code': course_code, "student": student, 'plans':plans, 'form': form})


def add_course_view(plan, course, semester_number):
    semester_field = f'semester_{semester_number}'
    semester = getattr(plan, semester_field)
    semester.courses.add(course)
    plan.save()

