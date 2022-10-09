

from django.urls import path

from . import views

urlpatterns = [
    path('get_blog_posts/' , views.get_blog_posts),
]
