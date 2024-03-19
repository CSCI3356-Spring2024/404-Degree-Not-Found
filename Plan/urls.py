from django.urls import path


from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView
from Plan.views import signup_view
from django.contrib.auth import views as auth_views
from Plan import views
from . import views

app_name = "Plan"
urlpatterns = [
    #path("", views.LandingView.as_view(), name="landing"),
    path('admin/', admin.site.urls),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('landing/', views.landing_view, name='landing'),
]
