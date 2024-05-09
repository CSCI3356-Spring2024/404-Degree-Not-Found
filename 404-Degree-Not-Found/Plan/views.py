from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic 
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.urls import reverse_lazy
from django.contrib.auth import login, logout
from .forms import EditStudentInfo, AddCourseToPlan, RemoveCourseFromPlan
from .models import Student, Admin, Plan, Advisor
from .api import fetch_course_data, fetch_courses
from django.core.paginator import Paginator
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from .data import MAJOR_COURSE_MAP
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from datetime import datetime
from .major_requirements import validate_major_requirements
from .get_next_semester import get_current_semester, get_upcoming_semesters, get_total_semesters
from .university_requirements import validate_university_requirements


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
    #testing if user is an advisor or a student, redirects to
    try:
        advisor = Advisor.objects.get(email=request.user.email)
        return redirect('Plan:admin_landing')
    except Advisor.DoesNotExist:
        pass

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
        # Total Credits
        completed = credits_completed(primary_plan, int(student.entered))
        credits_percentage = round((completed / credits_required) * 100)
        
        taken_courses = courses_completed(primary_plan,int(student.entered))

        # Major 1
        num_finished_req, num_req_needed, errormessages = validate_major_requirements(primary_plan, student.major, taken_courses)
        major_percentage = round((num_finished_req / num_req_needed) * 100)

        # Major 2
        if student.major2 == "Undeclared":
            num_finished_req2, num_req_needed2, errormessages2 = 0,0,[]
            major2_percentage = 0
        else:
            num_finished_req2, num_req_needed2, errormessages2 = validate_major_requirements(primary_plan, student.major2, taken_courses)
            major2_percentage = round((num_finished_req2 / num_req_needed2) * 100)
    
        # University Core
        num_finished_req_univ, num_req_needed_univ, errormessages_univ = validate_university_requirements(primary_plan, taken_courses)
        univ_percentage = round((num_finished_req_univ / num_req_needed_univ) * 100)
    else:
        current_credits = 0
        credits_percentage = 0
        major_percentage = 0
        major2_percentage = 0
        univ_percentage = 0

    return render(request, 'Landing.html', {'student': student, 'plans': plans, 'credits_percentage':credits_percentage, 'major_percentage':major_percentage, 'major2_percentage':major2_percentage, 'univ_percentage': univ_percentage}) 

def admin_landing_view(request):
    user = request.user
    try:
        advisor = Advisor.objects.get(email=user.email)
    except Advisor.DoesNotExist:
        return redirect('Plan:landing')

    primary_plans = Plan.objects.filter(s1__isnull=False, is_primary=True)

    course_data = {}

    for plan in primary_plans:
        entry_year = plan.student.entered
        current_semester, _ = get_current_semester(entry_year)
        total_semesters = get_total_semesters(entry_year)
        semesters = get_upcoming_semesters(current_semester, total_semesters)
        for semester_num, semester_name in semesters.items():
            print(f"Processing Semester: {semester_name}")
            course_codes = plan.__dict__[semester_num]
            for course_code in course_codes:
                if course_code:
                    if semester_name not in course_data:
                        course_data[semester_name] = {}
                    if course_code in course_data[semester_name]:
                        course_data[semester_name][course_code] += 1
                    else:
                        course_data[semester_name][course_code] = 1

    report_data = []
    for semester, course_counts in course_data.items():
        for course_code, student_count in course_counts.items():
            course_info = fetch_course_data(course_code)
            if course_info:
                course_name = course_info.get('title', 'Unknown')
                course_number = course_info.get('course_code', 'Unknown')
                report_data.append({
                    'semester': semester,
                    'course_name': course_name,
                    'course_number': course_number,
                    'student_count': student_count
                })
            else:
                report_data.append({
                    'semester': semester,
                    'course_name': 'Unknown',
                    'course_number': course_code,
                    'student_count': student_count
                })


    report_data_sorted = sorted(report_data, key=lambda x: (int(x['semester'][-4:]), '0' if 'Spring' in x['semester'] else '1', x['semester'][:5]))

    return render(request, 'admin_landing.html', {'report_data': report_data_sorted})

def get_student_semesters(entry_year):
    current_year = datetime.now().year
    current_month = datetime.now().month
    entry_year = int(entry_year)

    entry_semester = "Fall" if current_month >= 8 else "Spring"

    years_since_entry = current_year - entry_year

    total_semesters = min(years_since_entry * 2, 8)


    semesters = {}

    for i in range(1, total_semesters + 1):
        if entry_semester == "Fall":
            year = entry_year + (i - 1) // 2
            semester_name = f"Fall {year}" if i % 2 == 1 else f"Spring {year + 1}"
        else:
            year = entry_year + (i - 1) // 2
            semester_name = f"Spring {year}" if i % 2 == 1 else f"Fall {year}"

        semester_code = f"s{i}"
        semesters[semester_code] = semester_name

    return semesters
    


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

def is_date_passed(year, month, day):
    current_date = datetime.now().date()
    input_date = datetime(year, month, day).date()
    return current_date > input_date

def credits_completed(plan, entered_year):
    completed_dates = [
        (entered_year,8,26),
        (entered_year+1,1,13),
        (entered_year+1,8,26),
        (entered_year+2,1,13),
        (entered_year+2,8,26),
        (entered_year+3,1,13),
        (entered_year+3,8,26),
        (entered_year+4,1,13)  
    ]
    plan_objects = [plan.s1, plan.s2,plan.s3,plan.s4,plan.s5,plan.s6,plan.s7,plan.s8]
    completed_credits = 0
    for semester, dates in zip(plan_objects, completed_dates):
        if is_date_passed(dates[0],dates[1],dates[2]):
            for coursecode in semester:
                data = fetch_course_data(coursecode)
                completed_credits += data["credits"]
        else:
            break
    return completed_credits

def courses_completed(plan,entered_year):
    completed_dates = [
        (entered_year,8,26),
        (entered_year+1,1,13),
        (entered_year+1,8,26),
        (entered_year+2,1,13),
        (entered_year+2,8,26),
        (entered_year+3,1,13),
        (entered_year+3,8,26),
        (entered_year+4,1,13)  
    ]

    plan_objects = [plan.s1, plan.s2,plan.s3,plan.s4,plan.s5,plan.s6,plan.s7,plan.s8]
    courses_taken = []
    for semester, dates in zip(plan_objects, completed_dates):
        if is_date_passed(dates[0],dates[1],dates[2]):
            for coursecode in semester:
                courses_taken.append(coursecode)
    return courses_taken


def prereq_scanner(request, plan_id, plan_num):
    user = request.user
    student = Student.objects.get(email=user.email)
    user_entered_year = int(student.entered)
    plan = get_object_or_404(Plan, student=student, id=plan_id)
    total_credits = plan.total_credits
    semester_nums = ['s1', 's2', 's3', 's4', 's5', 's6', 's7', 's8']
    all_courses = set()

    courses_by_semester = {}
    for semester_num in semester_nums:
        course_codes = getattr(plan, semester_num, [])
        courses_by_semester[semester_num] = course_codes
        all_courses.update(course_codes)

    prereq_conflict = False
    for semester_num in sorted(semester_nums):
        course_list = courses_by_semester[semester_num]
        for course_code in course_list:
            course_data = fetch_course_data(course_code)
            prerequisites = course_data.get('prerequisites', [])
            if any(prereq not in all_courses for prereq in prerequisites):
                prereq_conflict = course_code
                break
        if prereq_conflict:
            break
    return prereq_conflict

def future_plan_view(request, plan_id, plan_num):

    user = request.user
    student = Student.objects.get(email=user.email)
    try:
        user_entered_year = int(student.entered) if student.entered.isdigit() else None
    except ValueError:
        user_entered_year = None  
    if user_entered_year is None:
        return HttpResponseBadRequest("Invalid data for 'entered' year.")

    plan = get_object_or_404(Plan, student=student, id=plan_id)
    total_credits = plan.total_credits

    completed_credits = credits_completed(plan, user_entered_year)
    student_major = student.major
    student_major2 = student.major2

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
    
    prereq_conflict = prereq_scanner(request, plan_id, plan_num)
    num_finished_req, num_req_needed, errormessages = validate_major_requirements(plan, student_major)
    num_finished_req2, num_req_needed2, errormessages2 = validate_major_requirements(plan, student_major2)
    num_finished_req3, num_req_needed3, errormessages3 = validate_university_requirements(plan)

    is_valid = num_finished_req >= num_req_needed
    is_valid2 = num_finished_req2 >= num_req_needed2
    is_valid3 = num_finished_req3 >= num_req_needed3

    return render(request, 'futureplan.html', {'student': student, 'plan': plan, 'semester_nums': semester_nums, 'courses_by_semester':courses_by_semester,'semester_names': semester_names, 'plan_id': plan_id, 'plan_num': plan_num, 'total_credits': total_credits, 'completed_credits': completed_credits, "is_valid": is_valid, "is_valid2":is_valid2, "is_valid3":is_valid3,"prereq_conflict": prereq_conflict, "errormessages": errormessages, "errormessages2": errormessages2,"errormessages3": errormessages3})


def course_list_view(request, plan_id, plan_num):
    user = request.user
    student = Student.objects.get(email=user.email)
    course_code = request.GET.get('course_code', '')
    courses_list = fetch_courses(course_code) if course_code else []

    paginator = Paginator(courses_list, 10)  # Show 10 courses per page.
    page_number = request.GET.get('page')
    courses = paginator.get_page(page_number)

    message, color = "", ""
    if request.method == 'POST':
        form = AddCourseToPlan(request.POST, student=student)
        if form.is_valid():
            try:
                form.save(student)
                message = "Course added successfully"
                color = "green"
            except ValidationError as e:
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
    else:
        form = AddCourseToPlan(student=student) 

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
            else:
                # If the plan_id is not in the selected plans list or the corresponding checkbox is not checked
                # Retrieve the Plan object using the plan_id
                plan = Plan.objects.get(id=plan_id)
                # Set the plan as non-primary
                plan.is_primary = False
                plan.save()
        
        return redirect('Plan:landing')  # Redirect to a relevant URL after processing

from django.urls import reverse

from django.http import HttpResponseRedirect
from django.urls import reverse

def remove_course(request):
    if request.method == 'POST':
        form = RemoveCourseFromPlan(request.POST)
        if form.is_valid():
            plan_id = form.cleaned_data['plan_id']
            plan_num = form.cleaned_data['plan_num']
            semester_num = form.cleaned_data['semester_num'] 
            if form.remove_course():
                return redirect('Plan:futureplan', plan_id, plan_num)
            else:
                print('Failed to remove course. Course or plan not found.')
        else:
            print('Form is not valid. Errors:', form.errors)
    else:
        print('Request method is not POST.')

    return HttpResponseRedirect(reverse('Plan:landing'))

def prereq_scanner(request, plan_id, plan_num):
    user = request.user
    student = Student.objects.get(email=user.email)
    user_entered_year = int(student.entered)
    plan = get_object_or_404(Plan, student=student, id=plan_id)
    total_credits = plan.total_credits
    semester_nums = ['s1', 's2', 's3', 's4', 's5', 's6', 's7', 's8']
    all_courses = set()

    courses_sem = {}
    for indx, semester_num in enumerate(semester_nums):
        course_codes = getattr(plan, semester_num, [])
        for each in course_codes:
            courses_sem[each] = indx

    prereq_conflict = False
    for semester_num in semester_nums:
        course_list = getattr(plan, semester_num, [])
        for course_code in course_list:
            course_data = fetch_course_data(course_code)
            prerequisites = course_data.get('prerequisites', [])
            for prereq in prerequisites:
                if prereq not in courses_sem:
                    prereq_conflict = course_code
                    break
                if courses_sem[prereq] >= courses_sem[course_code]:
                    prereq_conflict = course_code
                    break
        if prereq_conflict:
            break
    return prereq_conflict
    


