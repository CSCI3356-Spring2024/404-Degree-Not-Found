from django import forms
from django.core.exceptions import ValidationError
from .models import Student

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