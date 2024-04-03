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
    path("", views.login_view, name='login'),
    path('admin/', admin.site.urls),
    #path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('landing/', views.landing_view, name='landing'),
    path('profile/', views.profile_view, name='profile'),
    path('futureplan/', views.future_plan_view, name='futureplan'),
    path('courses/', views.courses_view, name='courses'),

    path("logout", views.logout_view)
]