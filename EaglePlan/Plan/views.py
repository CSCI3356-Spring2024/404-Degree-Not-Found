from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic 
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy

<<<<<<< HEAD
from .models import Name
class SignUpView(generic.CreateView):
	template_name = '/Registration/signup.html'
=======

>>>>>>> a06ce33 (Signup Page)

	form_class = UserCreationForm
	success_url = reverse_lazy('login')

#def home_view(request, *args, **kwargs):
# 	print(args, kwargs)
# 	print(request.user)
# 	#return HttpResponse('<h1>Hello World</h1>') #string of HTML code
# 	return render(request, 'home.html', {}) 

<<<<<<< HEAD
class LandingView(generic.CreateView):
     #links to the html code in "plan/Landing.html"
 	template_name = "plan/Landing.html"
# 	model = Name

=======
class LandingView(generic.ListView):
    #links to the html code in "polls/index.html"
    template_name = "plan/Landing.html"
		
class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'
>>>>>>> a06ce33 (Signup Page)
