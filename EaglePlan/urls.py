from django.contrib import admin
from django.urls import include, path
from Plan import views

#DO NOT USE THIS FOR APP SPECIFIC URLS!!!!!
#include() chops off whatever part of the URL matched up to that point and sends the remaining string to the included URLconf for further processing.
urlpatterns = [
    #path("", views.LandingView.as_view(), name="landing"),
    path('admin/', admin.site.urls),
    path('', include('Plan.urls')),
]
