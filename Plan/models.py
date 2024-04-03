from django.db import models

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
