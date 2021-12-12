

from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.ProfileView.as_view(), name='Profile_View') # To Create/Edit/Delete/GEt
]
