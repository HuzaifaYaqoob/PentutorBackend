from django.db import models
import uuid
from django.db.models import base
from django.utils.timezone import now

from django.contrib.auth.models import User
from Utility.models import Country, City

# Create your models here.


class Profile(models.Model):

    TYPE_CHOICES = [
        ('Student', 'Student'),
        ('Tutor', 'Tutor')
    ]

    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Others', 'Others'),

    ]

    user = models.OneToOneField( User, on_delete=models.DO_NOTHING, blank=True, related_name='user_profile')
    name = models.CharField(max_length=200, default='')
    user_type = models.CharField(choices=TYPE_CHOICES, default='Student', max_length=20)

    mobile = models.CharField(max_length=22, null=True, blank=True, default='')

    Country = models.ForeignKey(Country , on_delete=models.SET_NULL , null=True ,  blank=True )
    city = models.ForeignKey(City , on_delete=models.SET_NULL , null=True ,  blank=True )
    area = models.CharField(max_length=500, default='')
    date_of_birth = models.DateField(default=None, blank=True, null=True)
    gender = models.CharField(choices=GENDER_CHOICES, default='Male', max_length=10)
    detail = models.TextField(default='')
    qualification = models.CharField(max_length=200, default='')

    profile_image = models.ImageField(upload_to='images/profile_images/')
    degree_image = models.ImageField(upload_to='images/degree_images/')
    cnic_image = models.ImageField(upload_to='images/cnic_images/')

    slug = models.UUIDField(primary_key=True, unique=True, editable=False, auto_created=True, default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now=now)



class StudentProfile(Profile):
    subject = models.CharField(max_length=500, default='')
    institute = models.CharField(max_length=1000, default='')
    teaching_method = models.CharField(max_length=1000, default='')
    study_days = models.CharField(max_length=1000, default='')
    study_timing = models.CharField(max_length=1000,  default='')

    def __str__(self):
        return self.name

class TeacherProfile(Profile):
    # This is Profile Model for Teacher Role 

    def __str__(self) :
        return self.name