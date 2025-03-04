import uuid
from django.db import models

from django.contrib.auth.models import User
# from djrichtextfield.models import RichTextField
from ckeditor.fields import RichTextField

# Create your models here.


class BlogPost(models.Model):
    slug = models.UUIDField(primary_key=True, unique=True, editable=False, auto_created=True, default=uuid.uuid4)
    # user = models.ForeignKey(User, on_delete=models.CASCADE, default=None, null=True, blank=True, related_name='user_blog_posts')
    title = models.CharField(max_length=255, null=True, blank=True)
    image = models.ImageField(upload_to='blog/images/')
    description = RichTextField()
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        """
        Return a string representation of the BlogPost.

        Returns:
            str: The title of the BlogPost.
        """
        return str(self.title)