from django.db import models

from django.utils.timezone import now
import uuid
from django.contrib.auth.models import User
# Create your models here.


class CourseCategory(models.Model):
    slug = models.UUIDField(primary_key=True, unique=True, editable=False, auto_created=True, default=uuid.uuid4)
    title = models.CharField(max_length=500, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return str(self.slug)
    

class Course(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None, null=True, blank=True, related_name='user_courses')

    title = models.CharField(max_length=500, default='')
    short_title = models.CharField(max_length=300, default='')
    language = models.CharField(max_length=100, default='')
    course_category = models.ForeignKey(CourseCategory, null=True, blank=True, on_delete=models.CASCADE)
    level = models.CharField(default='', max_length=200)

    price = models.PositiveIntegerField(default=0)
    discount_price = models.PositiveIntegerField(default=0)

    description = models.TextField(default='')
    things_you_will_learn = models.TextField(default='')

    slug = models.UUIDField(primary_key=True, unique=True, editable=False, auto_created=True, default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now=now)

    def __str__(self):
        return str(self.slug)

class CourseMedia(models.Model):

    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course_medias')
    image = models.ImageField(upload_to='course/images/')

    slug = models.UUIDField(primary_key=True, unique=True, editable=False, auto_created=True, default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now=now)

    def __str__(self):
        return str(self.slug)



class CourseChapter(models.Model):
    title = models.CharField(max_length=500, default='')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course_chapters')
    slug = models.UUIDField(primary_key=True, unique=True, editable=False, auto_created=True, default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now=now)

    def __str__(self):
        return str(self.slug)



class ChapterVideo(models.Model):
    title = models.CharField(max_length=500, default='')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course_videos')
    chapter = models.ForeignKey(CourseChapter, on_delete=models.CASCADE, related_name='chapter_videos')
    video = models.FileField(upload_to='courses/chapter/videos/')
    vid_thumbnail = models.ImageField(upload_to='course/chapter/video_thumbnails/')
    duration = models.CharField(default='', max_length=200)
    slug = models.UUIDField(primary_key=True, unique=True, editable=False, auto_created=True, default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now=now)

    def __str__(self):
        return str(self.slug)


class CourseReview(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course_reviews')

    slug = models.UUIDField(primary_key=True, unique=True, editable=False, auto_created=True, default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now=now)

    def __str__(self):
        return str(self.slug)