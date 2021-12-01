


from django.urls import path, include

from . import views

urlpatterns = [
    path('login/', views.LoginAPI , name='LoginAPI'),
    path('user/' , views.UserAPI.as_view() , name='USER'),
    path('register/' , views.RegisterAPI , name='RegisterAPI')
]
