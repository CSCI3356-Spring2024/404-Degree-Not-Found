from django.contrib import admin

# Register your models here.
from .models import Student, Advisor, Plan

admin.site.register(Student)
admin.site.register(Advisor)
admin.site.register(Plan)