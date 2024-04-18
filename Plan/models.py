from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.

#user class, all users inherit this class since the information is consistent throughout
class User(models.Model):
    first_name = models.CharField(max_length = 100)
    last_name = models.CharField(max_length = 100)
    email = models.CharField(max_length = 200)

#student class, this is where the majors, minors, school, start data and other information lives
class Student(User):
    major = models.CharField(max_length = 100, default="None")
    major2 =  models.CharField(max_length = 100, default="None")
    minor = models.CharField(max_length = 100, default="None")
    minor2 = models.CharField(max_length = 100, default="None")
    grad_year = models.CharField(max_length = 100)
    entered = models.CharField(max_length = 100)
    school = models.CharField(max_length = 200, default="N/A")
    

class Advisor(User):
    department = models.CharField(max_length = 200, default=" ")
    school = models.CharField(max_length = 200, default=" ")
    pass

class Admin(User):
    pass

class Course(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=20)
    credits = models.IntegerField(default=3)

SEMESTER_CHOICES = [
    ('1', 'Freshman Fall'),
    ('2', 'Freshman Spring'),
    ('3', 'Sophomore Fall'),
    ('4', 'Sophomore Spring'),
    ('5', 'Junior Fall'),
    ('6', 'Junior Spring'),
    ('7', 'Senior Fall'),
    ('8', 'Senior Spring'),
]

class Semester(models.Model):
    semester_num = models.CharField(max_length=2, choices=SEMESTER_CHOICES, default="1")
    courses = models.ManyToManyField(Course)

class Plan(models.Model):
    user = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='plans')
    plan_number = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(3)])
    semesters = models.ManyToManyField(Semester)

    class Meta:
        unique_together = ('user', 'plan_number')


