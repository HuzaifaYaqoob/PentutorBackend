

from django.urls import path, include

from . import views

urlpatterns = [
    path('get_all_courses/' , views.get_all_courses),
    path('create_course/' , views.create_course),
    path('delete_course/' , views.delete_course),
    path('update_course/' , views.update_course),
    
    path('get_all_category/' , views.get_all_category),
    path('create_course_chapter/' , views.create_course_chapter),
    path('create_chapter_video/' , views.create_chapter_video),
    path('create_course_media/' , views.create_course_media),

    
]
