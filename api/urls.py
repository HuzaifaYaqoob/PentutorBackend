

from django.urls import path, include


urlpatterns = [
    path('authentication/', include('Authentication.urls'), name='Authentication'),
    path('profile/', include('Profile.urls'), name='Profile_url'),
    path('course/', include('Course.urls'), name='Profile_url'),
    path('utility/' , include('Utility.urls') , name='Utility_Names'),
    path('video_chat/' , include('VideoChat.urls') , name='VideoChatAPIS'),
    path('blog/' , include('Blog.urls') , name='BlogAppURLs'),
    path('job/' , include('Job.urls') , name='JobAPiUrls'),
]
