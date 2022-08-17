

from django.urls import path, include

from . import views

urlpatterns = [
    path('get_all_courses/' , views.get_all_courses),
    
]
