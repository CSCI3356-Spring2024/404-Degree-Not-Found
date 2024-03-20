from django import forms
from .models import Student


#providing the forms to edit student information
class EditStudentInfo(forms.ModelForm):
    model = Student
    fields = ['school', 'major', 'major2', 'minor1', 'minor2', 'entered', 'grad_year']
