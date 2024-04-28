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
            semester_field = getattr(selected_plan, semester_num)
            if not semester_field:
                setattr(selected_plan, semester_num, [code])
            elif len(semester_field) < 5:
                semester_field.append(code)
            else:
                raise forms.ValidationError("Selected semester is already full.")
            
            # Update total credits based on the course credits
            data = fetch_course_data(code)
            course_credits = data['credits']  # You need to implement this function
            selected_plan.total_credits += course_credits

            selected_plan.save()
        else:
            raise forms.ValidationError("Invalid semester selected.")

class EditStudentInfo(forms.ModelForm):
    SCHOOL_CHOICES = [
        ('MCAS', 'MCAS'),
        ('CSOM', 'CSOM'),
        ('CSON', 'CSON'),
        ('LSEHD', 'LSEHD'),
    ]

    MAJOR_CHOICES = [
        ('None', 'None'),
        ('Computer Science', 'Computer Science'),
        ('Economics', 'Economics'),
        ('Math', 'Math')
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
        ('2024', '2024')
    ]

    GRAD_YEAR_CHOICES = [
        ('None', 'None'),
        ('2024', '2024'),
        ('2025', '2025'),
        ('2026', '2026'),
        ('2027', '2027'),
        ('2028', '2028')
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