import uuid
from django.db import models

from django.contrib.auth.models import User


# Create your models here.


class BlogPost(models.Model):
    slug = models.UUIDField(primary_key=True, unique=True, editable=False, auto_created=True, default=uuid.uuid4)
    # user = models.ForeignKey(User, on_delete=models.CASCADE, default=None, null=True, blank=True, related_name='user_blog_posts')
    title = models.CharField(max_length=255, null=True, blank=True)
    image = models.ImageField(upload_to='blog/images/')
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return str(self.title)