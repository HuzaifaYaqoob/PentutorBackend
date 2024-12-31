from django.db import models

# Create your models here.

from django.contrib.auth.models import User

class Job(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_jobs')
    title = models.CharField(max_length=999, default='')
    description = models.TextField()

    class_teach = models.CharField(max_length=999, default='')
    subject_teach = models.CharField(max_length=999, default='')
    method = models.CharField(max_length=999, default='')
    location = models.CharField(max_length=999, default='')
    experience = models.CharField(max_length=999, default='')
    salary = models.CharField(max_length=999, default='')
    gender = models.CharField(max_length=999, default='')
    time = models.TimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    is_deleted = models.BooleanField(default=False)

class JobDays(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='job_days')
    day = models.CharField(max_length=999, default='')


class ApplyJob(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='apply_jobs')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='apply_jobs')
    message = models.TextField()
    resume = models.FileField(upload_to='resume/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)