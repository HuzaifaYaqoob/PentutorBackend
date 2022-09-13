

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
    path('get_my_courses/' , views.get_my_courses),
    path('update_course_chapter/' , views.update_course_chapter),
    path('delete_course_chapter/' , views.delete_course_chapter),
    path('delete_chapter_video/' , views.delete_chapter_video),
    path('get_course_chapters/' , views.get_course_chapters),
    path('get_course/' , views.get_course),
    
    path('add_to_cart/' , views.add_to_cart),
    path('get_my_cart/' , views.get_my_cart),
    path('delete_cart/' , views.delete_cart),
    path('update_cart/' , views.update_cart),
    
    
    path('create_course_session/' , views.create_course_session),
    path('update_course_session/' , views.update_course_session),
    path('get_course_session/' , views.get_course_session),
    path('delete_course_session/' , views.delete_course_session),

    
]
