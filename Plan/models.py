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
    #description = models.TextField()

    def __str__(self):
        return self.name

class Semester(models.Model):
    semester_number = models.PositiveIntegerField(unique=True)
    courses = models.ManyToManyField(Course)

    def __str__(self):
        return f'Semester {self.semester_number}'

class Plan(models.Model):
    user = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='plans')
    plan_number = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(3)])
    unique_semesters = models.BooleanField(default=False)
    semester_1 = models.OneToOneField(Semester, related_name='freshman_fall', on_delete=models.CASCADE)
    semester_2 = models.OneToOneField(Semester, related_name='freshman_spring', on_delete=models.CASCADE)
    semester_3 = models.OneToOneField(Semester, related_name='sophomore_fall', on_delete=models.CASCADE)
    semester_4 = models.OneToOneField(Semester, related_name='sophomore_spring', on_delete=models.CASCADE)
    semester_5 = models.OneToOneField(Semester, related_name='junior_fall', on_delete=models.CASCADE)
    semester_6 = models.OneToOneField(Semester, related_name='junior_spring', on_delete=models.CASCADE)
    semester_7 = models.OneToOneField(Semester, related_name='senior_fall', on_delete=models.CASCADE)
    semester_8 = models.OneToOneField(Semester, related_name='senior_spring', on_delete=models.CASCADE)

    def __str__(self):
        return f'Plan for {self.user}'



