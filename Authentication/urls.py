


from django.urls import path, include

from . import views

urlpatterns = [
    path('login/', views.LoginAPI , name='LoginAPI'),
    path('register/' , views.RegisterAPI , name='RegisterAPI')
]
