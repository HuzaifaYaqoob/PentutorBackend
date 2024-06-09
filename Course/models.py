from django.db import models

from django.utils.timezone import now
import uuid
import tempfile
from django.contrib.auth.models import User
import uuid
from io import BytesIO
from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.contrib.auth import get_user_model
import random
import string
from Profile.models import TeacherProfile
Image.MAX_IMAGE_PIXELS = 933120000
# Create your models here.


def generate_video_thumbnail(temp_thumb):
    temp_thumb = Image.fromarray(temp_thumb)
    temp_thumb = temp_thumb.convert('RGB')
    img_width = temp_thumb.size[0]
    img_height = temp_thumb.size[1]
    x = img_width / 800
    img_height = int(img_height // x)
    temp_thumb = temp_thumb.resize((800, img_height))
    thumb_io = BytesIO()
    temp_thumb.save(thumb_io, format='JPEG', quality=80)
    random_digits_for_thumbnail = ''.join(
        random.SystemRandom().choice(string.hexdigits + string.hexdigits) for _ in range(10))
    inmemory_uploaded_file = InMemoryUploadedFile(file=thumb_io, field_name=None,
                                                name=f'thumnail_{random_digits_for_thumbnail}.jpeg', content_type='image/jpeg',
                                                size=thumb_io.tell(), charset=None)
    return inmemory_uploaded_file

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
    
    def save(self, *args, **kwargs):
        if self.video and not self.vid_thumbnail:
            temp_file = tempfile.NamedTemporaryFile(suffix='.mp4', delete=False)
            temp_path = temp_file.name
            with open(temp_path, 'wb+') as destination:
                 for chunk in self.video.chunks():
                           destination.write(chunk)


            from moviepy.editor import VideoFileClip
            
            clip = VideoFileClip(temp_path)
            temp_thumb = clip.get_frame(1)
            self.vid_thumbnail = generate_video_thumbnail(temp_thumb)
            self.duration = int(clip.duration)
        super(ChapterVideo, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.slug)
    
class CourseReview(models.Model):
    slug = models.UUIDField(primary_key=True, unique=True, editable=False, auto_created=True, default=uuid.uuid4)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='coursereview_course')
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None, null=True, blank=True, related_name='coursereview_user')
    review = models.TextField(null=True, blank=True)
    rate = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return str(self.course)
    
    
class CartItem(models.Model):
    slug = models.UUIDField(primary_key=True, unique=True, editable=False, auto_created=True, default=uuid.uuid4)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='cartitem_course')
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None, null=True, blank=True, related_name='cartitem_user')
    quantity = models.IntegerField(default=1)
    
    created_at = models.DateTimeField(auto_now_add=True)
    course_cart = models.BooleanField(default=False)
    
    def __str__(self):
        return str(self.course)
    
class CourseDay(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True) 
    created_at = models.DateTimeField(auto_now_add=True)
    course_cart = models.BooleanField(default=False)
    
    def __str__(self):
        return str(self.name)
    
class CourseSession(models.Model):

    TYPE_CHOICE = [
        ('OnCampus', 'On Campus'),
        ('Online', 'Online'),
    ]
    DURATION_CHOICES = [
        ('TwoMonths', 'Two Months'),
        ('FourMonths', 'Four Months'),
        ('FiveMonths', 'Five Months'),
        ('SixMonths', 'Six Months'),
        ('MoreSixMonths', 'More than Six Months'),
    ]
    slug = models.UUIDField(primary_key=True, unique=True, editable=False, auto_created=True, default=uuid.uuid4)
    title = models.CharField(max_length=255, null=True, blank=True)
    instructor = models.ForeignKey(TeacherProfile, on_delete=models.CASCADE, null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='coursesession_course')
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None, null=True, blank=True, related_name='coursesession_user')
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    course_days = models.ManyToManyField(CourseDay, blank=True)
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    session_type = models.CharField(max_length=255, choices=TYPE_CHOICE, null=True, blank=True)
    duration = models.CharField(max_length=255, choices=DURATION_CHOICES, null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    course_cart = models.BooleanField(default=False)
    def __str__(self):
        return str(self.title)


class CoursePurchase(models.Model):
    slug = models.UUIDField(primary_key=True, unique=True, editable=False, auto_created=True, default=uuid.uuid4)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='bought_courses')
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None, null=True, blank=True, related_name='user_bought_courses')

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.slug)
