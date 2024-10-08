from django import forms
from django.core.exceptions import ValidationError
from .models import Student, Plan
from .api import fetch_course_data, fetch_courses

from .models import Plan

class AddCourseToPlan(forms.Form):
    code = forms.CharField(max_length=8)
    selected_semester = forms.ChoiceField(label='Select Semester', choices=[
        ('s1', 'Freshman Fall'),
        ('s2', 'Freshman Spring'),
        ('s3', 'Sophomore Fall'),
        ('s4', 'Sophomore Spring'),
        ('s5', 'Junior Fall'),
        ('s6', 'Junior Spring'),
        ('s7', 'Senior Fall'),
        ('s8', 'Senior Spring'),
    ], required=False)
    selected_plan = forms.ChoiceField(label='Select Plan', choices=[], required=False)

    def __init__(self, *args, **kwargs):
        student = kwargs.pop('student')
        super(AddCourseToPlan, self).__init__(*args, **kwargs)
        plans = Plan.objects.filter(student=student)
        plan_choices = [(plan.id, f'Plan {index+1}') for index, plan in enumerate(plans, start=0)]
        self.fields['selected_plan'].choices = plan_choices

    def save(self, student):
        code = self.cleaned_data['code']
        semester_num = self.cleaned_data['selected_semester']
        selected_plan_id = self.cleaned_data['selected_plan']
        print(selected_plan_id)
        
        try:
            selected_plan = Plan.objects.get(id=selected_plan_id, student=student)
        except Plan.DoesNotExist:
            raise forms.ValidationError("Selected plan does not exist for the current student.")
        
        # Add the course code to the selected semester field of the plan
        if hasattr(selected_plan, semester_num):
            # Number of credits for selected course
            data_selected = fetch_course_data(code)
            course_credits_selected = data_selected['credits']  # You need to implement this function

            semester_field = getattr(selected_plan, semester_num)
            print('SEM FIELD')
            print(semester_field)

            current_sem_credits = 0


            for coursecode in semester_field:
                data = fetch_course_data(coursecode)
                course_credits = data['credits']  # You need to implement this function
                current_sem_credits += course_credits
            current_sem_credits += course_credits_selected
            print(current_sem_credits)
            if not semester_field:
                setattr(selected_plan, semester_num, [code])
            elif code in semester_field:
                raise forms.ValidationError("You already have that course in the current semester.")
            elif current_sem_credits <= 18 and len(semester_field)<5:
                semester_field.append(code)
            else:
                raise forms.ValidationError("Selected semester is already full. Student may not take more than 18 credits and may not take more than 5 courses.")

            # Updating total credits
            selected_plan.total_credits += course_credits_selected

            selected_plan.save()
    
        else:
            raise forms.ValidationError("Invalid semester selected.")

# 
class RemoveCourseFromPlan(forms.Form):
    plan_id = forms.IntegerField(widget=forms.HiddenInput())
    plan_num = forms.CharField(widget=forms.HiddenInput())
    semester_num = forms.CharField(max_length=2, widget=forms.HiddenInput())
    course_id = forms.CharField(widget=forms.HiddenInput())

    def remove_course(self):
        plan_id = self.cleaned_data['plan_id']
        semester_num = self.cleaned_data['semester_num']
        course_id = self.cleaned_data['course_id']

        try:
            plan = Plan.objects.get(id=plan_id)
            courses_semester = getattr(plan, semester_num)
            if course_id in courses_semester:
                courses_semester.remove(course_id)

                # Update total credits based on the course credits
                data = fetch_course_data(course_id)
                course_credits = data['credits'] 
                plan.total_credits -= course_credits
                plan.save()
                return True
            else:
                return False  # Course not found in the semester
        except Plan.DoesNotExist:
            return False  # Plan not found
        
class EditStudentInfo(forms.ModelForm):
    SCHOOL_CHOICES = [
        ('MCAS', 'MCAS'),
        ('CSOM', 'CSOM'),
        ('CSON', 'CSON'),
        ('LSEHD', 'LSEHD'),
    ]

    MAJOR_CHOICES = [
        ('Undeclared', 'Undeclared'),
        ('Computer Science BA', 'Computer Science BA'),
        ('Computer Science BS', 'Computer Science BS'),
        ('Economics', 'Economics'),
        # ('Math', 'Math')
    ]

    MINOR_CHOICES = [
        ('None', 'None'),
        ('Studio Art', 'Studio Art'),
        ('Finance', 'Finance'),
    ]

    ENTERED_CHOICES = [
        ('None', 'None'),
        ('2020', '2020'),
        ('2021', '2021'),
        ('2022', '2022'),
        ('2023', '2023'),
    ]

    GRAD_YEAR_CHOICES = [
        ('None', 'None'),
        ('2024', '2024'),
        ('2025', '2025'),
        ('2026', '2026'),
        ('2027', '2027'),
    ]

    def validate_major(value):
        if value in ['', 'None']:
            raise ValidationError("Major 1 cannot be empty!")
    def validate_entered(value):
        if value in ['', 'None']:
            raise ValidationError("Entry year cannot be empty!")
    def validate_graduate(value):
        if value in ['', 'None']:
            raise ValidationError("Graduation year cannot be empty!")

    #form information that gets passed into the student model
    school = forms.ChoiceField(choices=SCHOOL_CHOICES)
    major = forms.ChoiceField(choices=MAJOR_CHOICES, validators=[validate_major])
    major2 = forms.ChoiceField(choices=MAJOR_CHOICES, required=False, label='Major 2')
    minor = forms.ChoiceField(choices=MINOR_CHOICES, required=False)
    minor2 = forms.ChoiceField(choices=MINOR_CHOICES, required=False, label='Minor 2')
    entered = forms.ChoiceField(choices=ENTERED_CHOICES, validators=[validate_entered], label='Entry Year')
    grad_year = forms.ChoiceField(choices=GRAD_YEAR_CHOICES, validators=[validate_graduate], label='Graduation Year')

    class Meta:
        model = Student
        fields = ['school', 'major', 'major2', 'minor', 'minor2', 'entered', 'grad_year']