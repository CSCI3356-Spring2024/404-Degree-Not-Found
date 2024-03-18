
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView
from Plan.views import SignUpView
from django.contrib.auth import views as auth_views
from Plan import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/returning/', auth_views.LoginView.as_view(), name='returning'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
]
