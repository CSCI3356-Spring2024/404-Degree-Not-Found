from django import forms
from .models import Student


#providing the forms to edit student information
class EditStudentInfo(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['school', 'major', 'major2', 'minor', 'minor2', 'entered', 'grad_year']
