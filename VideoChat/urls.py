
from django.urls import path

from . import views

urlpatterns = [
    path('create_video_chat/', views.create_video_chat),
    path('get_video_chat/', views.get_video_chat),
    path('get_user_video_chats/', views.get_user_video_chats),

    # Demo Call 
    path('request-tutor-demo-class/', views.requestTutorDemoClass),
    path('get_tutor_demo_classes_requests/', views.getTutorDemoCallRequest),
    path('get_student_demo_classes_requests/', views.getStudentDemoCallRequest),
    path('accept_reject_demo_class/<str:class_id>/', views.AcceptRejectClassRequest),
]
