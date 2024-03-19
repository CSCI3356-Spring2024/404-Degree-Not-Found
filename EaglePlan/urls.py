from django.contrib import admin
from django.urls import include, path
from Plan.views import SignUpView
from Plan import views
#include() chops off whatever part of the URL matched up to that point and sends the remaining string to the included URLconf for further processing.
urlpatterns = [
    path("Plan/", include("Plan.urls")),
    path('admin/', admin.site.urls),
    path('signup/', views.SignUpView.as_view(), name='signup'),
]
