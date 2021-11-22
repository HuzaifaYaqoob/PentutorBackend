


from django.urls import path, include

from . import views

urlpatterns = [
    path('login/', views.LoginAPI , name='LoginAPI'),
    path('user/' , views.RegisterAPI.as_view() , name='RegisterAPI')
]
