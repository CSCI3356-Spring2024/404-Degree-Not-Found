from django.contrib import admin

# Register your models here.
from .models import Student, Advisor, Course, Semester, Plan

admin.site.register(Student)
admin.site.register(Advisor)
admin.site.register(Course)
admin.site.register(Semester)
admin.site.register(Plan)