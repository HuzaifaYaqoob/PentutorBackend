

from django.urls import path, include

urlpatterns = [
    path('authentication/', include('Authentication.urls'), name='Authentication')
]
