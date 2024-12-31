


from django.urls import path, include

from . import views

urlpatterns = [
    path('create_job/', views.create_job),
    path('get_my_jobs/', views.get_my_jobs),
    path('get_jobs/', views.get_jobs),
    path('get_single_job/<str:job_id>/', views.get_single_job),
    path('apply_job/<str:job_id>/', views.apply_job),
]
