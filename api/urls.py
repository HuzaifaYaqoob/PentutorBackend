

from django.urls import path, include

urlpatterns = [
    path('authentication/', include('Authentication.urls'), name='Authentication'),
    path('profile/', include('Profile.urls'), name='Profile_url'),
    path('utility/' , include('Utility.urls') , name='Utility_Names')
]
