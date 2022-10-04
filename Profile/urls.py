

from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.ProfileView.as_view(), name='Profile_View'), # To Create/Edit/Delete/GEt
    path('get_all_tutors/' , views.get_all_tutors , name='get_allTutors'),
    path('get_tutor/' , views.get_tutor),
    path('get_featured_tutors/' , views.get_featured_tutors),
    
]
