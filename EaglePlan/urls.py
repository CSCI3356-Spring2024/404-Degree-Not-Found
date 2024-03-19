from django.contrib import admin
from django.urls import include, path
from Plan import views
#include() chops off whatever part of the URL matched up to that point and sends the remaining string to the included URLconf for further processing.
urlpatterns = [
    #path("", views.LandingView.as_view(), name="landing"),
    path('admin/', admin.site.urls),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('landing/', views.landing_view, name='landing'),
    path('', include('Plan.urls')),
    path('profile/', profile_view, name='profile'),
    path('future-plan/', future_plan_view, name='futureplan'),
]
