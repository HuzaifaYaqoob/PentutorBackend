import uuid
from django.db import models
from django.utils.timezone import now

# Create your models here.

class Subject(models.Model):
        slug = models.UUIDField(primary_key=True, unique=True, editable=False, auto_created=True, default=uuid.uuid4)
        name = models.CharField(max_length=200, default='')
        created_at = models.DateTimeField(auto_now=now)

        def __str__(self):
            return self.name
