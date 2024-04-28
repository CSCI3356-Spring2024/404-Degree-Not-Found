from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic 
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.urls import reverse_lazy
from django.contrib.auth import login, logout
from .forms import EditStudentInfo, AddCourseToPlan, RemoveCourseFromPlan
from .models import Student, Admin, Plan
from .api import fetch_course_data, fetch_courses
from django.core.paginator import Paginator
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from .data import MAJOR_COURSE_MAP
from django.core.exceptions import ValidationError
from django.http import JsonResponse


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

    if student.plan_set.count() < 3:
        for _ in range(3 - student.plan_set.count()):
            Plan.objects.create(student=student)

    plans = Plan.objects.filter(student=student)

    # Retrieve the primary plan for the student
    primary_plan = Plan.objects.filter(student=student, is_primary=True).first()

    credits_required = 120
    if primary_plan is not None:
        current_credits = primary_plan.total_credits
        credits_percentage = round((current_credits / credits_required) * 100,1)
    else:
        current_credits = 0
        credits_percentage = 0


    return render(request, 'Landing.html', {'student': student, 'plans': plans, 'credits_percentage':credits_percentage}) 


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

def future_plan_view(request, plan_id, plan_num):
    user = request.user
    student = Student.objects.get(email=user.email)
    plan = get_object_or_404(Plan, student=student, id=plan_id)
    total_credits = plan.total_credits

    semester_names = {
        's1': 'Freshman Fall',
        's2': 'Freshman Spring',
        's3': 'Sophomore Fall',
        's4': 'Sophomore Spring',
        's5': 'Junior Fall',
        's6': 'Junior Spring',
        's7': 'Senior Fall',
        's8': 'Senior Spring',
    }

    semester_nums = ['s1', 's2', 's3', 's4', 's5', 's6', 's7', 's8']


    # courses_by_semester = [(semester_num, getattr(plan, semester_num, [])) for semester_num in semester_nums]
    courses_by_semester = []
    for semester_num in semester_nums:
        course_codes = getattr(plan, semester_num, [])
        course_tuple_list = []
        for coursecode in course_codes:
            data = fetch_course_data(coursecode)
            course_title = data["title"]
            course_tuple = (coursecode, course_title)
            course_tuple_list.append(course_tuple)
        courses_by_semester.append((semester_num, course_tuple_list))
    
    print(courses_by_semester)

    return render(request, 'futureplan.html', {'student': student, 'plan': plan, 'semester_nums': semester_nums, 'courses_by_semester':courses_by_semester,'semester_names': semester_names, 'plan_id': plan_id, 'plan_num': plan_num, 'total_credits': total_credits})


def course_list_view(request, plan_id, plan_num):
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
            try:
                form.save(student)
                print("Form data:", form.cleaned_data)
                print("Course added to the plan successfully.")
                message = "Course added successfully"
                color = "green"
            except ValidationError as e:
                print("Course failed to add")
                message = e.message
                color = "red"
            finally:
                return render(request, 'course_list.html', {
                    'plan_id': plan_id,
                    'plan_num': plan_num,
                    'courses': courses,
                    'course_code': course_code,
                    'student': student,
                    'form': form,
                    'message': message,
                    'color': color
                })
        else:
            form = AddCourseToPlan(student=student)
            print("Form errors:", form.errors)
            print("Course not added to plan")
    else:
        form = AddCourseToPlan(student=student) 
        print("Request method is not POST")

    return render(request, 'course_list.html', {
        'plan_id': plan_id,
        'plan_num': plan_num,
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

def set_primary_plan(request):
    if request.method == 'POST':
        # Retrieve the selected plans and their associated plan IDs
        selected_plans = request.POST.getlist('checkbox')

        # Get all Plan IDs
        all_plan_ids = [plan.id for plan in Plan.objects.all()]

        # Process each plan
        for plan_id in all_plan_ids:
            # If the plan_id is in the selected plans list and the corresponding checkbox is checked
            if str(plan_id) in selected_plans:
                # Retrieve the Plan object using the plan_id
                plan = Plan.objects.get(id=plan_id)
                # Set the plan as primary
                plan.is_primary = True
                plan.save()
                print(f"Selected primary plan successfully: Plan ID {plan_id}")
            else:
                # If the plan_id is not in the selected plans list or the corresponding checkbox is not checked
                # Retrieve the Plan object using the plan_id
                plan = Plan.objects.get(id=plan_id)
                # Set the plan as non-primary
                plan.is_primary = False
                plan.save()
                print(f"Deselected primary plan successfully: Plan ID {plan_id}")
        
        return redirect('Plan:landing')  # Redirect to a relevant URL after processing

from django.urls import reverse

from django.http import HttpResponseRedirect
from django.urls import reverse

def remove_course(request):
    if request.method == 'POST':
        form = RemoveCourseFromPlan(request.POST)
        if form.is_valid():
            plan_id = form.cleaned_data['plan_id']  # Assuming you have plan_id in your form
            plan_num = form.cleaned_data['plan_num']
            semester_num = form.cleaned_data['semester_num']  # Assuming you have plan_num in your form
            if form.remove_course():
                print('Course removed successfully.')
                # Assuming you have access to plan_id and plan_num in your view
                return HttpResponseRedirect(reverse('Plan:futureplan', kwargs={'plan_id': plan_id, 'plan_num': plan_num}))
            else:
                print('Failed to remove course. Course or plan not found.')
        else:
            print('Form is not valid. Errors:', form.errors)
            print(form)
    else:
        print('Request method is not POST.')

    # If the form submission fails or the request method is not POST, redirect to some page
    return HttpResponseRedirect(reverse('Plan:landing'))  # Redirect to landing page

    


