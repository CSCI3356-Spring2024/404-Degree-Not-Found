from django.db import models

# Create your models here.

#user class, all users inherit this class since the information is consistent throughout
class User(models.Model):
    first_name = models.CharField(max_length = 100)
    last_name = models.CharField(max_length = 100)
    email = models.CharField(max_length = 200)
    school = models.CharField(max_length = 200)
    department = models.CharField(max_length = 200)


#student class, this is where the majors, minors, school, start data and other information lives
class Student(User):
    major = models.CharField(max_length = 100, default="Undecided")
    major2 =  models.CharField(max_length = 100, default="NA")
    minor = models.CharField(max_length = 100, default="NA")
    minor2 = models.CharField(max_length = 100, default="NA")
    grad_year = models.CharField(max_length = 100)
    entered = models.CharField(max_length = 100)

class Advisor(User):
    pass

class Admin(User):
    pass
