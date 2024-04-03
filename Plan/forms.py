from django import forms
from django.core.exceptions import ValidationError
from .models import Student

class EditStudentInfo(forms.ModelForm):
    SCHOOL_CHOICES = [
        ('MCAS', 'MCAS'),
        ('CSOM', 'CSOM'),
    ]

    MAJOR_CHOICES = [
        ('None', 'None'),
        ('Computer Science', 'Computer Science'),
        ('Economics', 'Economics'),
    ]

    MINOR_CHOICES = [
        ('None', 'None'),
        ('Studio Art', 'Studio Art'),
        ('Finance', 'Finance'),
    ]

    ENTERED_CHOICES = [
        ('2020', '2020'),
        ('2021', '2021'),
        ('2022', '2022'),
        ('2023', '2023'),
    ]

    GRAD_YEAR_CHOICES = [
        ('2024', '2024'),
        ('2025', '2025'),
        ('2026', '2026'),
        ('2027', '2027'),
    ]

    def validate_major(value):
        if value in ['', 'None']:
            raise ValidationError("Major 1 cannot be empty")

    #form information that gets passed into the student model
    school = forms.ChoiceField(choices=SCHOOL_CHOICES)
    major = forms.ChoiceField(choices=MAJOR_CHOICES, validators=[validate_major])
    major2 = forms.ChoiceField(choices=MAJOR_CHOICES, required=False)
    minor = forms.ChoiceField(choices=MINOR_CHOICES, required=False)
    minor2 = forms.ChoiceField(choices=MINOR_CHOICES, required=False)
    entered = forms.ChoiceField(choices=ENTERED_CHOICES)
    grad_year = forms.ChoiceField(choices=GRAD_YEAR_CHOICES)

    class Meta:
        model = Student
        fields = ['school', 'major', 'major2', 'minor', 'minor2', 'entered', 'grad_year']