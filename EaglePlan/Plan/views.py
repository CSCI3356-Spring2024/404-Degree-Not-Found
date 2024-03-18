from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect

class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'

def home_view(request, *args, **kwargs):
	print(args, kwargs)
	print(request.user)
	#return HttpResponse('<h1>Hello World</h1>') #string of HTML code
	return render(request, 'home.html', {}) 
